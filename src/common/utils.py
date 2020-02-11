""" Утилиты хелперы """
import uuid
import json
import functools

from aiohttp import web


def serialize_helpers(obj):
    """Нестандартные функции сериализации для сложных типов"""
    if isinstance(obj, uuid.UUID):
        return obj.hex
    raise TypeError('Unable to serialize {!r}'.format(obj))


json_dumps = functools.partial(json.dumps, default=serialize_helpers)
json_response = functools.partial(web.json_response, dumps=json_dumps)

GOOD_RES = (200, 201)


class ResponseTemplate:
    """Ответ сериализованный в JSON"""
    def __init__(self, status: int, addition={}, description={}, result=None):
        if result is None:
            self.result = True if status in GOOD_RES else False
        else:
            self.result = result
        self.status = status
        self.addition = addition
        self.description = description

    def response(self):
        """Формирует стандартный ответ для АПИ в виде JSON.
        Формат JSON ответа:
            {
                "status": int (http код ответа)
                "result": bool (результат операции)
                "addition": JSON (поля для описания текущей операции)
                "description": JSON (прочие текстовые поля)
            }
        """
        return json_response({
            "status": self.status,
            "result": self.result,
            "addition": self.addition,
            "description": self.description
        }, status=self.status)
