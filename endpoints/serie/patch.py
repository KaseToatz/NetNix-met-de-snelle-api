from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchSerie(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), genre_id: int = Form(), resolution: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Serie WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This serie does not exist."}, 400)
                await cursor.execute("UPDATE Serie SET title = %s, genre_id = %s, resolution = %s WHERE id = %s", (title, genre_id, resolution, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchSerie:
    return PatchSerie(app, Method.PATCH, "/serie/patch", JSONResponse)