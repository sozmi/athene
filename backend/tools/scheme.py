"""
Файл содержит описание конфигурационной схемы приложения
"""
from schema import Or, Schema


def get_config_schema():
    """
    Получение схемы конфигурационного файла
    :return: схема конфигурационного файла
    """
    schema = {
        "app":
            {
                "name": str
            },
        "parser":
            {
                "small-image": bool,
                "header": {
                    "default": str,
                    "generate": bool
                }
            }
    }
    return Schema(schema)