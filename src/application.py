import aiomysql
import asyncio
import os

from fastapi import FastAPI
from importlib import import_module
from starlette.middleware.base import BaseHTTPMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from .exceptions import MissingSetupFunction
from . import Connection, HTTPMiddleware

class App(FastAPI):

    def __init__(self, title: str, db: Connection) -> None:
        super().__init__(title=title, redoc_url=None, root_path="/api/v1")
        self._db = db
        self.pool: aiomysql.Pool = None
        self.pwdContext = CryptContext(schemes=["bcrypt"])
        self.oauthScheme = OAuth2PasswordBearer("token")
        self.add_event_handler("startup", self._startup)
        self.add_middleware(BaseHTTPMiddleware, dispatch=HTTPMiddleware(self))

    async def _startup(self) -> None:
        try:
            self.pool = await aiomysql.create_pool(user=self._db.username, password=self._db.password, host=self._db.host, port=self._db.port, db=self._db.database, loop=asyncio.get_event_loop())
        except:
            raise
        for root, _, files in os.walk("endpoints"):
            for file in files:
                if file.endswith(".py"):
                    self.addEndpoint(os.path.join(root, file).replace("\\", ".").replace("/", ".")[:-3])

    def addEndpoint(self, path: str) -> None:
        module = import_module(path)
        setup = getattr(module, "setup", None)
        if not setup:
            raise MissingSetupFunction
        endpoint = setup(self)
        self.add_api_route(endpoint.path, endpoint.callback, response_class=endpoint.responseClass, methods=[endpoint.method.name], name=endpoint.__class__.__qualname__)