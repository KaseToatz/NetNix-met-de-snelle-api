import cv2

from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchMovie(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), genre_id: int = Form(), filepath: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title, duration, genre_id, filepath, resolution FROM Movie WHERE id = %s", (id,))
                movie = await cursor.fetchone()
                if not movie:
                    return JSONResponse({"error": "This movie does not exist."}, 400)
                dbtitle, duration, dbfilepath, dbgenre_id, resolution = await cursor.fetchone()
                if filepath != dbfilepath:
                    duration = int(cv2.VideoCapture(filepath).get(cv2.CAP_PROP_POS_MSEC) / 1000)
                    height = cv2.VideoCapture(filepath).get(cv2.CAP_PROP_FRAME_WIDTH)
                    if height >= 2160:
                        resolution = "UHD"
                    elif height >= 1440:
                        resolution = "QHD"
                    elif height >= 1080:
                        resolution = "FHD"
                    elif height >= 720:
                        resolution = "HD"
                    else:
                        resolution = "SD"
                await cursor.execute("UPDATE Movie SET title = %s, duration = %s, filepath = %s, genre_id = %s, resolution = %s WHERE id = %s", (title or dbtitle, duration, filepath or dbfilepath, genre_id or dbgenre_id, resolution, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchMovie:
    return PatchMovie(app, Method.PATCH, "/movie/patch", JSONResponse)