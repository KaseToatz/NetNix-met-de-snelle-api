import os
import datetime

from fastapi import Request
from typing import Coroutine, Any, Callable
from jose import jwt

from .exceptions import DatabaseNotConnected

SIGNING_KEY = os.getenv("SIGNING_KEY")

class HTTPMiddleware:

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, request: Request, callNext: Coroutine) -> Any:
        if not self.app.pool:
            raise DatabaseNotConnected
        else:
            return await callNext(request)
        
class Connection:

    def __init__(self, username: str, password: str, host: str, port: int, database: str) -> None:
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

async def isAuthorized(token: str, check: Callable[[str], bool]) -> bool:
    data = jwt.decode(token, SIGNING_KEY, algorithms=["bcrypt"])
    return datetime.datetime.fromtimestamp(data["exp"]) > datetime.datetime.utcnow() and check(data["sub"])