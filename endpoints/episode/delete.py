from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeleteEpisode(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Episode WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This episode does not exist."}, 400)
                await cursor.execute("DELETE FROM Episode WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeleteEpisode:
    return DeleteEpisode(app, Method.DELETE, "/episode/delete", JSONResponse)