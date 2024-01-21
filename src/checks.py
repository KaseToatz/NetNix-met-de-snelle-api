import datetime
import os

from jose import jwt

from .utils import Connection
from .enums import UserType

SIGNING_KEY = os.getenv("SIGNING_KEY")

class Authorization:

    def __init__(self, email: str, usertype: UserType) -> None:
        self.email = email
        self.usertype = usertype

class Checks:

    async def getAuthorization(self, token: str | None, admin: bool = False) -> Authorization | None:
        if token:
            data = jwt.decode(token, SIGNING_KEY, algorithms=["bcrypt"])
            if datetime.datetime.fromtimestamp(data["exp"]) > datetime.datetime.utcnow():
                async with Connection() as db:
                    async with db.cursor() as cursor:
                        if admin:
                            await cursor.execute("SELECT role FROM Admin WHERE email = %s", (data["sub"],))
                            result = await cursor.fetchone()
                            if result:
                                return Authorization(data["sub"], UserType(result[0]))
                        else:
                            await cursor.execute("SELECT email FROM Account WHERE email = %s", (data["sub"],))
                            if await cursor.fetchone():
                                return Authorization(data["sub"], UserType.DEFAULT)