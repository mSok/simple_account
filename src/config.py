"""Конфигурация подключения к БД"""
import os
import logging

# Параметры коннекта к БД
db = {
    'user': os.getenv('DB_USER') or 'postgres',
    'password': os.getenv('DB_PASSWORD') or '',
    'host': os.getenv('DB_HOST') or 'localhost',
    'database': os.getenv('DB_NAME') or 'account',
}

# Уровень логирования
logging = getattr(logging, os.getenv('LOG', '').upper() or 'WARNING', None)
