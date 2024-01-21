from typing import Any
from fastapi.responses import Response
from passlib.context import CryptContext

from . import Method
from .checks import Checks

class Endpoint:

    def __init__(self, method: Method, path: str, responseClass: Response) -> None:
        self.checks = Checks()
        self.jwt = CryptContext(["bcrypt"])
        self.method = method
        self.path = path
        self.responseClass = responseClass

    async def callback(self) -> Any:
        raise NotImplementedError