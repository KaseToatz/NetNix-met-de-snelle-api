from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetAllEpisodesFromSerie(Endpoint):

    async def callback(self, serie_id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id, title FROM Episode WHERE serie_id = %s", (serie_id))
                episodes = await cursor.fetchall()
                if not episodes:
                    return JSONResponse({"error": "There aren't any episodes in this serie yet."}, 400)
                episode_list = [{"id": episode[0], "title": episode[1]} for episode in episodes]
                return JSONResponse({episode_list})
            
def setup(app : App) -> GetAllEpisodesFromSerie:
    return GetAllEpisodesFromSerie(app, Method.GET, "/episode/getAllFromSerie", JSONResponse)