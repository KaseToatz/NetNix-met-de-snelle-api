import aiomysql
import asyncio

from fastapi import FastAPI
from importlib import import_module
from starlette.middleware.base import BaseHTTPMiddleware

from .exceptions import MissingSetupFunction
from . import Connection, HTTPMiddleware

class App(FastAPI):

    def __init__(self, title: str, db: Connection) -> None:
        super().__init__(title=title, redoc_url=None, swagger_ui_oauth2_redirect_url=None)
        self._db = db
        self.pool: aiomysql.Pool = None
        self.add_event_handler("startup", self._startup)
        self.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware(self))

    async def _startup(self) -> None:
        try:
            self.pool = await aiomysql.create_pool(user=self._db.username, password=self._db.password, host=self._db.host, port=self._db.port, db=self._db.database, loop=asyncio.get_event_loop())
        except:
            pass

    def addEndpoint(self, path: str) -> None:
        module = import_module(path)
        try:
            endpoint = module.setup(self)
            self.add_api_route(endpoint.path, endpoint.callback, response_class=endpoint.responseClass, methods=[endpoint.method.name])
        except:
            raise MissingSetupFunction