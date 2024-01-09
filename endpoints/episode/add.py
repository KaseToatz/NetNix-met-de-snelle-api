from fastapi.responses import JSONResponse
from fastapi import Form
import cv2

from src import App, Endpoint, Method

class AddEpisode(Endpoint):

    async def callback(self, title: str = Form(), serie_id: int = Form(), season: int = Form(), filepath: str = Form()) -> JSONResponse:
        duration = int(cv2.VideoCapture(filepath).get(cv2.CAP_PROP_POS_MSEC) / 1000)

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title FROM Episode WHERE title = %s AND duration = %s", (title, duration))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This episode already exists."}, 400)
                await cursor.execute("SELECT id FROM Serie WHERE id = %s", (serie_id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "The season you are trying to add the episode to does not exist."})
                await cursor.execute("INSERT INTO Episode(title, duration, serie_id, season, filepath) VALUES(%s, %s, %s, %s, %s)", (title, duration, serie_id, season, filepath))
                return JSONResponse({})
            
def setup(app : App) -> AddEpisode:
    return AddEpisode(app, Method.POST, "/episode/add", JSONResponse)