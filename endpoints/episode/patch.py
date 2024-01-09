from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchEpisode(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), serie_id: int = Form(), season: int = Form(), filepath: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Episode WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This episode does not exist."}, 400)
                await cursor.execute("UPDATE Episode SET title = %s, serie_id = %s, season = %s, filepath = %s WHERE id = %s", (title, serie_id, season, filepath, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchEpisode:
    return PatchEpisode(app, Method.PATCH, "/episode/patch", JSONResponse)