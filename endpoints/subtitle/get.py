from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetSubtitle(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Subtitle WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This subtitle does not exist."}, 400)
                await cursor.execute("SELECT * FROM Subtitle WHERE id = %s", (id,))
                _, filepath, language, movie_id, serie_id = await cursor.fetchone()
                return JSONResponse({"id": id, "filepath": filepath, "language": language, "movie_id": movie_id, "serie_id": serie_id})
            
def setup(app : App) -> GetSubtitle:
    return GetSubtitle(app, Method.GET, "/subtitle/get", JSONResponse)