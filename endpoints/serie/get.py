from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class GetSerie(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Serie WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This serie does not exist."}, 400)
                await cursor.execute("SELECT * FROM Serie WHERE id = %s", (id,))
                _, title, genre_id, resolution = await cursor.fetchone()
                return JSONResponse({"id": id, "title": title, "genre_id": genre_id, "resolution": resolution})
            
def setup() -> GetSerie:
    return GetSerie(Method.GET, "/serie/get", JSONResponse)