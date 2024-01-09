from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddSerie(Endpoint):

    async def callback(self, title: str = Form(), genre_id: int = Form(), resolution: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title FROM Serie WHERE title = %s", (title,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This serie already exists."}, 400)
                await cursor.execute("INSERT INTO Serie(title, genre_id, resolution) VALUES(%s, %s, %s)", (title, genre_id, resolution))
                return JSONResponse({})
            
def setup(app : App) -> AddSerie:
    return AddSerie(app, Method.POST, "/serie/add", JSONResponse)