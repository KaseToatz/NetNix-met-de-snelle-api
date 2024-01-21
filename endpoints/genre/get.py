from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class GetGenre(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Genre WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This genre does not exist."}, 400)
                await cursor.execute("SELECT * FROM Genre WHERE id = %s", (id,))
                _, description = await cursor.fetchone()
                return JSONResponse({"id": id, "description": description})
            
def setup() -> GetGenre:
    return GetGenre(Method.GET, "/serie/get", JSONResponse)