import logging
import asyncpg

import config


async def connect_db(app):
    # Пул соединений
    try:
        logging.debug('Try create connection pool')
        app['pool'] = await asyncpg.create_pool(**config.db)
    except Exception as exc:
        logging.error(exc)
