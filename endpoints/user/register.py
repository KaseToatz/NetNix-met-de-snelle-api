from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class RegisterUser(Endpoint):
    
    async def callback(self, email: str = Form(), password: str = Form()) -> JSONResponse:
        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT email FROM Account WHERE email = %s", (email,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "User with this email already exists."}, 400)
                await cursor.execute(
                    "INSERT INTO Account(email, password, payment_method, banned, subscription, referred_by_account, active) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (email, password, None, 0, 0, None, 1)
                )
                return JSONResponse({})

def setup(app: App) -> RegisterUser:
    return RegisterUser(app, Method.POST, "/user/register", JSONResponse)