""" Утилиты валидаторы """
import uuid


class DBException(Exception):
    """Ошибка подключения к БД"""
    def __init__(self, message):
        self.message = message


def uuid_validate(account_id):
    if isinstance(account_id, uuid.UUID):
        return account_id
    else:
        try:
            account_id = uuid.UUID(account_id)
        except Exception as exc:
            raise exc


def db_validate(request):
    pool = request.app.get('pool')
    if not pool:
        raise DBException('Service broken (db not connected)')
    return pool
