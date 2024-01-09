import datetime

from fastapi.responses import JSONResponse
from fastapi import Form
from jose import jwt

from src import App, Endpoint, Method

SIGNING_KEY = "5c4215af1d278962457562717b41fc3061671d1981e07ee37fd20afa5d5ca08c"

class RegisterUser(Endpoint):
    
    async def callback(self, email: str = Form(), password: str = Form()) -> JSONResponse:
        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id, password FROM Account WHERE email = %s", (email,))
                result = await cursor.fetchone()
                if not result:
                    return JSONResponse({"error": "User with this email does not exist."}, 400)
                if not self.app.pwdContext.verify(password, result[1]):
                    return JSONResponse({"error": "Password does not match."}, 401)
                return JSONResponse({"token": jwt.encode({"sub": result[0], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SIGNING_KEY)})

def setup(app: App) -> RegisterUser:
    return RegisterUser(app, Method.POST, "/user/login", JSONResponse)