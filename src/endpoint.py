from typing import Any
from fastapi.responses import Response

from . import Method, Checks

class Endpoint:

    def __init__(self, method: Method, path: str, responseClass: Response) -> None:
        self.checks = Checks()
        self.method = method
        self.path = path
        self.responseClass = responseClass

    async def callback(self) -> Any:
        raise NotImplementedError