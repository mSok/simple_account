"""Конфигурация подключения к БД"""
import os
import logging

# Параметры коннекта к БД
db = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
}

# Уровень логирования
logging = getattr(logging, os.getenv('LOG').upper() or 'WARNING', None)
