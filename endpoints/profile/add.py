from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddProfile(Endpoint):

    async def callback(self, account_id: int = Form(), name: str = Form(), age: int = Form(), image_filepath: str = Form(), language: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM Acount WHERE id = %s", (account_id,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This acount does not exist."}, 400)
                await cursor.execute("INSERT INTO Profile(account_id, name, age, image_filepath, language) VALUES(%s, %s, %s, %s, %s)", (account_id, name, age, image_filepath, language))
                return JSONResponse({})
            
def setup(app : App) -> AddProfile:
    return AddProfile(app, Method.POST, "/profile/add", JSONResponse)