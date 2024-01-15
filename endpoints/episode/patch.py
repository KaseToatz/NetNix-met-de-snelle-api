import cv2

from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchEpisode(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), serie_id: int = Form(), season: int = Form(), filepath: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title, duration, serie_id, season, filepath FROM Episode WHERE id = %s", (id,))
                episode = await cursor.fetchone()
                if not episode:
                    return JSONResponse({"error": "This episode does not exist."}, 400)
                dbtitle, duration, dbserie_id, dbseason, dbfilepath = await cursor.fetchone()
                if filepath != dbfilepath:
                    duration = int(cv2.VideoCapture(dbfilepath).get(cv2.CAP_PROP_POS_MSEC) / 1000)
                await cursor.execute("UPDATE Episode SET title = %s, duration = %s, serie_id = %s, season = %s, filepath = %s WHERE id = %s", (title or dbtitle, duration, serie_id or dbserie_id, season or dbseason, filepath or dbfilepath, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchEpisode:
    return PatchEpisode(app, Method.PATCH, "/episode/patch", JSONResponse)