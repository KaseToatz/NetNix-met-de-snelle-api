from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetProfile(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Profile WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This profile does not exist."}, 400)
                await cursor.execute("SELECT * FROM Profile WHERE id = %s", (id,))
                _, account_id, name, age, image_filepath, language = await cursor.fetchone()
                return JSONResponse({"id": id, "account_id": account_id, "name": name, "age": age, "image_filepath": image_filepath, "language": language})
            
def setup(app : App) -> GetProfile:
    return GetProfile(app, Method.GET, "/profile/get", JSONResponse)