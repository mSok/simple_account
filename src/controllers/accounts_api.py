from aiohttp import web
from common.utils import ResponseTemplate
from common import validators
from models.account import Account


async def ping(request: web.Request):
    """Роут проверки работоспособности сервиса"""
    try:
        pool = validators.db_validate(request)
    except validators.DBException as exc:
        return ResponseTemplate(500, None, {'message': exc.message}).response()

    async with pool.acquire() as conn:
        acc = await conn.fetch("SELECT * FROM accounts")
        print(acc)
    return ResponseTemplate(200, None,  {'message': 'Service started 🚀'}).response()


async def add(request: web.Request):
    """Метод пополнения баланса уже созданного счета.

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
    pool = request.app['pool']
    payload = await request.json()
    async with pool.acquire() as conn:
        return await Account(conn).substract(payload.get('account_id'), payload.get('amount'))


async def get_status(request: web.Request):
    pool = request.app['pool']
    payload = await request.json()
    async with pool.acquire() as conn:
        return await Account(conn).get_status(payload.get('account_id'))


    #     user = await user_conn.get_user(**payload)
    #     if user is None:
    #         return web.json_response(ResponseTemplate(request=request,
    #                                                   result='Fail',
    #                                                   description='uuid not found or incorrect').to_dict(), status=404)
    #     result = await user_conn.balance_substraction(**payload)
    #     if result is None:
    #         return web.json_response(ResponseTemplate(request=request,
    #                                                   result='Fail',
    #                                                   description='insufficient funds').to_dict(), status=400)
    # return web.json_response(ResponseTemplate(request=request, result='OK', addition=result).to_dict())
