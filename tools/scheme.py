from schema import Or, Schema


def get_config_schema():
    """
    Получение схемы конфигурационного файла
    :return: схема конфигурационного файла
    """
    schema = {
        "app": {
            "name": str,
            "mode": Or("console", "web", "app")
        }
    }
    return Schema(schema)