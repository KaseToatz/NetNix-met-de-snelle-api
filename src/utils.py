from fastapi import Request
from typing import Coroutine, Any

from .exceptions import DatabaseNotConnected

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