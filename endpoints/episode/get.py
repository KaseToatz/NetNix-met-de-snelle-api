from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetEpisode(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Episode WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This episode does not exist."}, 400)
                await cursor.execute("SELECT * FROM Episode WHERE id = %s", (id,))
                _, title, duration, serie_id, season, filepath = await cursor.fetchone()
                return JSONResponse({"id": id, "title": title, "duration": duration, "serie_id": serie_id, "season": season, "filepath": filepath})
            
def setup(app : App) -> GetEpisode:
    return GetEpisode(app, Method.GET, "/episode/get", JSONResponse)