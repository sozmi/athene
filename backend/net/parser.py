import json
import logging as log
import os
import uuid
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

from db.repos.image_repository import add_url_to_image, select_all_url, select_all_non_verify_images, create_image
from defenitions import ROOT_DIR
from net.validator import ValidatorException, ValidatorCode
from tools import awaits


class Parser:
    """
    Класс-парсер изображений с яндекс-картинок
    """

    def __init__(self, pm):
        self.validator = None
        self.proxy = pm
        self.fake_header = Headers(browser="chrome", os="win", headers=True)
        self.small_image = None
        self.header = None
        self.generate_header = True

    def set_validator(self, validator):
        if self.validator != validator:
            self.validator = validator

    def __parse_page(self, page, query):
        """
        Разбор кода html страницы
        @page - номер страницы
        @query - запрос
        """

        # получаем содержимое страницы
        div = None
        while div is None:
            content = self.__get_html(page, query)
            root = BeautifulSoup(content, 'html.parser')
            div = root.find('div', class_="Root",
                            id=lambda x: x and x.startswith('ImagesApp-'))
            # проверка на капчу
            if div is None:
                print(f'Капча на {page} странице.')
                awaits(5)
                self.proxy.get_next()
                return None

        data_state = div.get('data-state')
        jdata = json.loads(data_state)
        jent = jdata['initialState']['serpList']['items']['entities']

        links = []
        # получаем url изображений
        for item in jent:
            # image - аватары изображений, originUrl - изображения в оригинальном формате
            if self.small_image:
                url = 'http:' + jent[item]['image']
                print(url)
                links.append(url)
            else:
                url = jent[item]['origUrl']
                print(url)
                links.append(url)

        return links

    def __get_html(self, page, query):
        """
        Получение кода html страницы
        @page - номер страницы
        @query - запрос
        """
        url = f'https://yandex.ru/images/touch/search?from=tabbar&p={page}&text={query}&itype=jpg'
        header = self.__get_headers()
        proxies = self.proxy.get()
        if proxies['http'] == '':
            log.info('Новая итерация по списку прокси')
            awaits(30)

        self.__print_info(url, proxies, header)

        try:
            response = requests.get(url, headers=header, timeout=(
                3, 10), proxies=proxies)
        except Exception as e:
            log.info('%s: %s', e.__class__.__name__, url)
            awaits(5)
            return self.__get_html(page, query)
        log.info('Подключились')
        return response.content

    def __get_headers(self):
        """
        Получение случайного заголовка страницы
        """
        header = self.header
        if self.generate_header:
            header = self.fake_header.generate()

        return header

    def __print_info(self, url, proxy, headers):
        """
        Выводим информацию о текущем подключении
        @url - ссылка по которой подключаемся
        @proxy - ip proxy
        @headers - заголовки строки подключения
        """

        print()
        print(f'URL: {url}')
        print(f'Proxy: {proxy}')
        print(f'Headers UA: {headers}')

    def __download(self, url, num_load=-1):
        """
        Скачивание изображения по ссылке
        @label - метка
        @url - ссылка на изображение
        @nameFile - название файла
        @num_load - количество попыток загрузки
        """
        max_num_load = 5  # максимальное число попыток загрузки
        num_load += 1
        if num_load > max_num_load:
            log.warning('Превышено максимальное количество загрузок')
            return False
        header = self.__get_headers()
        filename = f'{uuid.uuid1()}.jpg'
        while True:
            path = f'{ROOT_DIR}/data/temp/images/{filename}'
            if not os.path.exists(path):
                break
        try:
            with requests.get(url, headers=header, stream=True, timeout=(5, 15), verify=False) as r:
                with open(path, 'wb') as f:
                    f.write(r.content)
                    log.info('Скачан файл [%s]: %s', filename, url)
        except requests.exceptions.SSLError as e:
            # Узнаем имя возникшего исключения
            log.warning('%s: %s', e.__class__.__name__, url)
            return False
        except requests.exceptions.ConnectionError as e:
            # Узнаем имя возникшего исключения
            log.warning('%s: %s', e.__class__.__name__, url)
            awaits(5)
            return self.__download(url, num_load)
        except Exception as e:
            # Узнаем имя возникшего исключения
            log.error('%s: %s', e.__class__.__name__, url)
            awaits(3)
            return self.__download(url, num_load)

        try:
            self.validator.verify(path)
            return filename
        except ValidatorException as e:
            if e.code == ValidatorCode.ERR_CLONE:
                # если это клон запомним url
                add_url_to_image(filename, False, url)
            # в любом случае удалим временное изображение
            os.remove(path)
        return None

    def download_images(self, query, lid, need_count):
        """
        Ищем изображения по запросу
        @name - запрос
        @need_count - необходимое количество изображений
        """
        page = 0
        query = str.replace(query, ' ', '%20')
        urls_used = select_all_url()
        if urls_used is None: urls_used = []
        current_count = len(select_all_non_verify_images())

        # ищем ссылки на оригинальные изображения
        while current_count < need_count:
            urls_new = None
            while urls_new is None:
                urls_new = self.__parse_page(page, query)
                awaits(15)

            urls = list(set(urls_new) - set(urls_used))
            log.info('Найдено %s urls', len(urls))

            for url in urls:
                path = self.__download(url)
                if path:
                    today = datetime.today()
                    create_image(lid, path, url, today)
                    current_count += 1
            log.info('Загружено %d изображений из %d', {current_count}, {need_count})
            page += 1
        log.info('Все изображения для метки с id(%s) загружены', lid)