from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddSubtitle(Endpoint):

    async def callback(self, filepath: str = Form(), language: str = Form(), movie_id: int = Form(), serie_id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM Subtitle WHERE language = %s AND movie_id = %s AND serie_id = %s", (language, movie_id, serie_id))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This subtitle already exists."}, 400)
                await cursor.execute("INSERT INTO Subtitle(filepath, language, movie_id, serie_id) VALUES(%s, %s, %s, %s)", (filepath, language, movie_id, serie_id))
                return JSONResponse({})
            
def setup(app : App) -> AddSubtitle:
    return AddSubtitle(app, Method.POST, "/subtitle/add", JSONResponse)