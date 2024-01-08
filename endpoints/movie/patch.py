from fastapi.responses import JSONResponse
from fastapi import Form
import cv2

from src import App, Endpoint, Method

class PatchMovie(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), filepath: str = Form(), genre_id: int = Form()) -> JSONResponse:

        async with self.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Movie where movie WHERE id = %s", (id,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This movie does not exist."}, 400)
                await cursor.execute("UPDATE title = %s, filepath = %s, ")
                return JSONResponse({})
            
def setup(app : App) -> PatchMovie:
    return PatchMovie(app, Method.PATCH, "/movie/patch", JSONResponse)