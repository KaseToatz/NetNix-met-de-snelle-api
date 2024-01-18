from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddGenre(Endpoint):

    async def callback(self, description: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM Genre WHERE description = %s", (description,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This genre already exists."}, 400)
                await cursor.execute("INSERT INTO Genre(description) VALUES(%s)", (description))
                return JSONResponse({})
            
def setup(app : App) -> AddGenre:
    return AddGenre(app, Method.POST, "/genre/add", JSONResponse)