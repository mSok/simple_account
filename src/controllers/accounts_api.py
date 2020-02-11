from aiohttp import web
from common.utils import ResponseTemplate
from common import validators
from models.account import Account


async def ping(request: web.Request):
    """Роут проверки работоспособности сервиса"""
    try:
        _ = validators.db_validate(request)
    except validators.DBException as exc:
        return ResponseTemplate(500, None, {'message': exc.message}).response()
    return ResponseTemplate(200, None,  {'message': 'Service started 🚀'}).response()


async def add(request: web.Request):
    """Роут пополнения баланса

    Args:
        request(web.Request): запрос к АПИ, payload JSON форматa
            {
                "amount": "string",
                "account_id": "string"
            }

    Returns:
        JSON формата ResponseTemplate
    """
    pool = request.app['pool']
    payload = await request.json()
    async with pool.acquire() as conn:
        return await Account(conn).add(payload.get('account_id'), payload.get('amount'))


async def substract(request: web.Request):
    """Роут уменьшения баланса
    Args:
        request(web.Request): запрос к АПИ, payload JSON форматa
            {
                "amount": "string",
                "account_id": "string"
            }

    Returns:
        JSON формата ResponseTemplate
    """
    pool = request.app['pool']
    payload = await request.json()
    async with pool.acquire() as conn:
        return await Account(conn).substract(payload.get('account_id'), payload.get('amount'))


async def get_status(request: web.Request):
    """Роут статус счета
    Args:
        request(web.Request): запрос к АПИ, payload JSON форматa
            {
                "amount": "string",
                "account_id": "string"
            }

    Returns:
        JSON формата ResponseTemplate
    """
    pool = request.app['pool']
    payload = await request.json()
    async with pool.acquire() as conn:
        return await Account(conn).get_status(payload.get('account_id'))
