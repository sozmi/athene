import multiprocessing

import uvicorn
from fastapi import FastAPI
from uvicorn import Config, Server

from db.scripts import create_db_and_tables
from endpoints.image import image_router
from endpoints.label import label_router
from endpoints.user import user_router
from endpoints.model import model_router
import logging as log

app = FastAPI()
app.include_router(label_router)
app.include_router(image_router)
app.include_router(user_router)
app.include_router(model_router)

class UvicornServer(multiprocessing.Process):

    def __init__(self, config: Config):
        super().__init__()
        self.server = Server(config=config)
        self.config = config

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        self.server.run()


def start():
    config = Config('main:app', host='localhost', reload=True)
    instance = UvicornServer(config=config)
    instance.start()
    yield instance
    instance.stop()


create_db_and_tables()

if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)