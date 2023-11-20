from typing import Any
from fastapi.responses import Response
from . import App, Method

class Endpoint:

    def __init__(self, app: App, method: Method, path: str, responseClass: Response) -> None:
        self.db = app.db
        self.method = method
        self.path = path
        self.responseClass = responseClass

    async def callback(self) -> Any:
        raise NotImplementedError