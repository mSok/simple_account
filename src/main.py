import asyncio
import logging
from aiohttp import web

import config
from common.db import connect_db
from controllers import accounts_api as api
from common.tasks import calc_balance


async def init_app():
    """Инициализируем приложение"""
    app = web.Application()
    # Подключится к БД
    await connect_db(app)
    # роуты API
    app.add_routes([
        web.get('/api/ping', api.ping),
        web.post('/api/add', api.add),
        web.post('/api/status', api.get_status),
        web.post('/api/substract', api.substract),
    ])
    return app


if __name__ == "__main__":

    logging.basicConfig(level=config.logging)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    # Запуск периодической таски ( раз в 10 минут пересчитываем баланс)
    loop.create_task(calc_balance(app['pool'], 60 * 10))
    logging.warning('Starting on 8080 ...')
    web.run_app(app, port=8080)
