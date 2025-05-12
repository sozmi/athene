"""
Файл системы запуска приложения
"""
import logging as log
import os
from yaml.parser import ParserError
from schema import SchemaError
import yaml

from backend.tools.scheme import get_config_schema
from backend.main import start as start_backend
from frontend.main import start as start_front

def get_config():
    """
    Получение и проверка конфигурационного файла приложения
    :return: конфигурационный файл
    """
    config_path = 'config.yaml'
    scheme_path = 'backend/tools/scheme.py'
    if not os.path.isfile(config_path):
        log.error('Отсутствует файл конфигурации %s', config_path)
        return
    if not os.path.isfile(config_path):
        log.error('Отсутствует файл схемы %s', scheme_path)
        return

    with open(config_path, encoding='utf-8') as file:
        try:
            data = yaml.safe_load(file)
            config_schema = get_config_schema()
            config_schema.validate(data)
        except ParserError as e:
            log.error('Проверьте синтаксис файла %s. Ошибка парсера: %s', config_path, e)
            return None
        except SchemaError as e:
            log.error('Проверьте файл %s на соответствие схеме. Возникла ошибка: %s', config_path, e)
            return None
        return data


def main():
    """
    Метод для начала работы системы запуска
    """
    log.getLogger().setLevel(log.INFO)
    data = get_config()
    if data is None:
        return

    app_name = data['app']['name']
    log.info('Программа запуска %s стартовала', app_name)
    log.info('Запуск бэкенда')
    start_backend()
    # create_db_and_tables()
    log.info('Запуск фронтенда')
    start_front()
    log.info('Программа запуска %s завершила работу', app_name)


if __name__ == '__main__':
    main()
