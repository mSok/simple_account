import os
import json
import asyncpg
import asyncio
import unittest

from models.account import Account


TEST_DB = {
    'user': os.getenv('DB_USER') or 'postgres',
    'password': os.getenv('DB_PASSWORD') or '',
    'host': os.getenv('DB_HOST') or 'localhost',
}
DB = 'test_account'


class TestAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.event_loop)

        async def async_setup():
            to_create = await asyncpg.connect(**TEST_DB, database='postgres')
            await to_create.execute(f''' DROP DATABASE {DB}; ''')
            await to_create.execute(f''' CREATE DATABASE {DB} ''')
            await to_create.close()
            cls._conn = await asyncpg.connect(**TEST_DB, database=DB)
            await cls._conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
            await cls._conn.execute('''CREATE TABLE IF NOT EXISTS public.accounts (
                id uuid DEFAULT public.uuid_generate_v4() PRIMARY KEY,
                fio character varying(225) NOT NULL,
                hold INT NOT NULL,
                current_balans INT NOT NULL,
                status boolean DEFAULT true
            );
            INSERT INTO public.accounts(id, fio, current_balans, hold, status)
            VALUES ('26c940a1-7228-4ea2-a3bc-e6460b172040', 'Петров Иван Сергеевич',1700, 300, True);

            INSERT INTO public.accounts(id, fio, current_balans, hold, status)
            VALUES ('7badc8f8-65bc-449a-8cde-855234ac63e1', 'Kazitsky Jason',200, 200, True);

            INSERT INTO public.accounts(id, fio, current_balans, hold, status)
            VALUES ('5597cc3d-c948-48a0-b711-393edf20d9c0', 'Пархоменко Антон Александрович',10, 300, True);

            INSERT INTO public.accounts(id, fio, current_balans, hold, status)
            VALUES ('867f0924-a917-4711-939b-90b179a96392', 'Петечкин Петр Измаилович',1000000, 1, False);
            ''')
        cls.event_loop.run_until_complete(async_setup())

    @classmethod
    def tearDownClass(cls):
        async def async_tear():
            await cls._conn.close()
        cls.event_loop.run_until_complete(async_tear())
        cls.event_loop.close()

    def test_status(self):
        async def async_test_status():
            t = await Account(self._conn).get_status('867f0924-a917-4711-939b-90b179a96392')
            assert t.status == 200
            res = json.loads(t.text)
            assert res['result'] is True
            assert res['addition']['status'] is False

            t = await Account(self._conn).get_status('26c940a1-7228-4ea2-a3bc-e6460b172040')
            assert t.status == 200
            res = json.loads(t.text)
            assert res['result'] is True
            assert res['addition']['status'] is True
        self.event_loop.run_until_complete(async_test_status())

    # TODO нужно дописать тест с конкурентным доступом
    def test_operations(self):
        async def async_test_op():
            _closed_acc = '867f0924-a917-4711-939b-90b179a96392'
            # Операции невозможно так как счет закрыт
            t = await Account(self._conn).substract(_closed_acc, 100)
            assert t.status == 400
            res = json.loads(t.text)
            assert res['result'] is False
            assert 'Ваш счет закрыт' in res['description']['message']

            t = await Account(self._conn).add(_closed_acc, 100)
            assert t.status == 400
            res = json.loads(t.text)
            assert res['result'] is False
            assert 'Ваш счет закрыт' in res['description']['message']

            # Невозможно, так как сумма больше баланса + hold
            _acc = '26c940a1-7228-4ea2-a3bc-e6460b172040'
            t = await Account(self._conn).get_status(_acc)
            res = json.loads(t.text)
            _t_hold = res['addition']['hold']
            _t_balans = res['addition']['current_balans']
            ct = await Account(self._conn).substract(_acc, _t_balans - _t_hold + 1)
            self.assertEqual(ct.status, 400, 'Ошибка операции substract')

            ct = await Account(self._conn).substract(_acc, _t_balans)
            self.assertEqual(ct.status, 400, 'Ошибка операции substract')

            ct = await Account(self._conn).substract(_acc, _t_balans - _t_hold)
            self.assertEqual(ct.status, 200, 'Ошибка операции substract')
            t = await Account(self._conn).get_status(_acc)
            res = json.loads(t.text)
            # баланс не изменится, изменится hold
            self.assertEqual(res['addition']['current_balans'], _t_balans, 'Ошибка баланса')
            # баланс не изменится, изменится hold
            self.assertEqual(res['addition']['hold'], _t_balans, 'Ошибка баланса')

            # Не валидные данные
            nt = await Account(self._conn).add(_acc, -100)
            self.assertEqual(nt.status, 400, 'Ошибка операции add')

            nt = await Account(self._conn).add(_acc, 0)
            self.assertEqual(nt.status, 200, 'Ошибка операции add')

        self.event_loop.run_until_complete(async_test_op())


if __name__ == '__main__':
    unittest.main()
