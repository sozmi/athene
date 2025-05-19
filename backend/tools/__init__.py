import os
from time import sleep

def awaits(sec):
    """
    Ожидание с выводом в консоль
    @sec - количество секунд
    """
    for i in range(sec, 0, -1):
        print(f'Ждем: {i:03} s', end='\r')
    sleep(1)

def iter_file(path):
    with open(path, 'rb') as f:
        yield from f


def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)