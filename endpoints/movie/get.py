from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetMovie(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Movie WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This movie does not exist."}, 400)
                await cursor.execute("SELECT FROM Movie WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> GetMovie:
    return GetMovie(app, Method.GET, "/movie/get", JSONResponse)