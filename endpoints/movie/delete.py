from fastapi.responses import JSONResponse
from fastapi import Form
import cv2

from src import App, Endpoint, Method

class DeleteMovie(Endpoint):

    async def callback(self, title: str = Form(), filepath: str = Form()) -> JSONResponse:
        duration = int(cv2.VideoCapture(filepath).get(cv2.CAP_PROP_POS_MSEC) / 1000)

        async with self.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title FROM Movie where movie WHERE title = %s AND duration = %s", (title, duration))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This movie does not exists."}, 400)
                await cursor.execute("DELETE FROM Movie WHERE title = %s AND duration = %s", (title, duration))
                return JSONResponse({})
            
def setup(app : App) -> DeleteMovie:
    return DeleteMovie(app, Method.DELETE, "/movie/delete", JSONResponse)