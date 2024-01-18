from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchSubtitle(Endpoint):

    async def callback(self, id: int = Form(), filepath: str = Form(), language: str = Form(), movie_id: int = Form(), serie_id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT filepath, language, movie_id, serie_id FROM Subtitle WHERE id = %s", (id,))
                subtitle = await cursor.fetchone()
                if not subtitle:
                    return JSONResponse({"error": "This subtitle does not exist."}, 400)
                dbfilepath, dblanguage, dbmovie_id, dbserie_id = await cursor.fetchone() 
                await cursor.execute("UPDATE Subtitle SET filepath, language, movie_id, serie_id WHERE id = %s", (filepath or dbfilepath, language or dblanguage, movie_id or dbmovie_id, serie_id or dbserie_id, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchSubtitle:
    return PatchSubtitle(app, Method.PATCH, "/subtitle/patch", JSONResponse)