from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchMovie(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), filepath: str = Form(), genre_id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Movie WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This movie does not exist."}, 400)
                await cursor.execute("UPDATE Movie SET title = %s, filepath = %s, genre_id = %s WHERE id = %s", (title, filepath, genre_id, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchMovie:
    return PatchMovie(app, Method.PATCH, "/movie/patch", JSONResponse)