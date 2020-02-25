from asyncio import sleep
import asyncpg

from models.account import Account


async def calc_balance(pool: asyncpg.pool.Pool, timeout: int):
    """ Периодеческая таска по уменьшению баланса на размер замороженных средств

    Args:
        pool (An instance of asyncpg.pool.Pool): пул соеденений к БД
        timeout (int): задержка перед вычетанием hold в секундах
    """
    while True:
        await sleep(timeout)
        async with pool.acquire() as conn:
            await Account(conn).calc_balance()
