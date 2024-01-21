from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method, Connection

class RegisterUser(Endpoint):
    
    async def callback(self, email: str = Form(), password: str = Form(), referrer: int = Form(None)) -> JSONResponse:
        async with Connection() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT email FROM Account WHERE email = %s", (email,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "User with this email already exists."}, 400)
                await cursor.callproc("add_account", (email, self.app.pwdContext.hash(password), None, 0, None, referrer, 1))
                return JSONResponse({})

def setup() -> RegisterUser:
    return RegisterUser(Method.POST, "/user/register", JSONResponse)