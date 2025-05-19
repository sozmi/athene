import logging as log
import os
import cv2

from enum import Enum

class ValidatorCode(Enum):
    ERR_OPEN = 100
    ERR_EDIT = 200
    ERR_CLONE = 300
    ERR_SIZE = 400

class ValidatorException(Exception):
    def __init__(self, err, code):
        self.err = err
        self.code = code

    def __str__(self):
        return f'{self.code}: {self.err}'

class Validator:
    def __init__(self, dirs_images, size_image):
        self.dirs = dirs_images
        self.size = size_image

    def verify_size(self, image):
        height, width, channels = image.shape
        size = (width, height)
        return size == self.size

    def verify(self, path_image):
        image = cv2.imread(path_image)
        if image is None:
            err = 'Не удалось открыть изображение!'
            log.warning(err)
            raise ValidatorException(err, ValidatorCode.ERR_OPEN)

        image = cv2.resize(image, self.size)
        cv2.imwrite(path_image, image)
        if image is None:
            err = 'Не удалось открыть измененное изображение!'
            log.warning(err)
            raise ValidatorException(err, ValidatorCode.ERR_EDIT )

        for dir in self.dirs:
            file_names = os.listdir(dir)
            for file_name in file_names:
                path_file = f'{dir}/{file_name}'
                if path_image == path_file:
                    continue
                exist_image = cv2.imread(path_file)
                if exist_image is None:
                    err = f'Не удалось открыть измененное изображение {path_file}!'
                    log.warning(err)
                    raise ValidatorException(err, ValidatorCode.ERR_EDIT)
                if not self.verify_size(exist_image):
                    exist_image = cv2.resize(exist_image, self.size)
                    cv2.imwrite(path_file, exist_image)
                if (image == exist_image).all():
                    err = 'Такое изображение уже было загружено!'
                    log.warning(err)
                    raise ValidatorException(err, ValidatorCode.ERR_CLONE)
