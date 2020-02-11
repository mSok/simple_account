# TODO Комментарии пересмотреть, написать валидаторы и тесты. + периодичная таска не готова
import uuid
from decimal import Decimal, InvalidOperation
from common.utils import ResponseTemplate


class Account:
    """Класс модель данных счета"""
    ADD_FIELDS = ("account_id", "amount")

    def __init__(self, conn):
        self._conn = conn

    async def add(self, account_id: uuid.UUID, amount):
        try:
            amount = Decimal(amount)
            if amount < 0:
                raise ValueError('Пополнять баланс можно только положительной суммой')
            if account_id is None or amount is None:
                raise TypeError('Некорректные входные данные')
        except (InvalidOperation, ValueError, TypeError) as exc:
            return ResponseTemplate(400, None, {'message': str(exc)}).response()

        try:
            res = await self._conn.fetchrow('''
                UPDATE accounts
                SET current_balans = current_balans + $1
                WHERE id = $2 RETURNING *''', amount, account_id)
        except Exception as exc:
            return ResponseTemplate(500, None, {'message': str(exc)}).response()

        if not res:
            return ResponseTemplate(404, None, {'message': '🚫 Счет не найден!'}).response()

        return ResponseTemplate(
            status=200,
            addition=dict(res)
        ).response()

    async def get_status(self, account_id):
        """ Получить информацию по счету

        Args:
            account_id (uuid): идентификатор счета

        Returns:
            JSON формата ResponseTemplate
        """
        if not account_id:
            return ResponseTemplate(400, None, {'message': 'Type Error'}).response()

        try:
            res = await self._conn.fetchrow('SELECT * FROM accounts WHERE id = $1', account_id)
        except Exception as exc:
            return ResponseTemplate(500, None, {'message': str(exc)}).response()
        if not res:
            return ResponseTemplate(404, None, {'message': '🚫 Счет не найден!'}).response()

        return ResponseTemplate(200, dict(res)).response()

    async def substract(self, account_id, amount):
        # TODO Возможно есть смысл сделать через SELECT FOR UPDATE
        res = await self._conn.fetchrow('''
            UPDATE accounts
            SET hold = hold + $1
            WHERE id = $2
                AND current_balans - hold - $1 > 0
            RETURNING *
        ''', amount, account_id)
        if not res:
            return ResponseTemplate(400, None, {'message': 'Недостаточно средств'}).response()
        return ResponseTemplate(200, dict(res)).response()
