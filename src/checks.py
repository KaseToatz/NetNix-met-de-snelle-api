import datetime
import os

from typing import Callable
from jose import jwt

SIGNING_KEY = os.getenv("SIGNING_KEY")

class Checks:

    async def isAuthorized(self, token: str, checks: list[Callable[[str], bool]]) -> bool:
        data = jwt.decode(token, SIGNING_KEY, algorithms=["bcrypt"])
        return datetime.datetime.fromtimestamp(data["exp"]) > datetime.datetime.utcnow() and all([check(data["sub"]) for check in checks])
    
    async def isAdmin(self, email: str) -> bool:
        ...