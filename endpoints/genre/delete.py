from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeleteGenre(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Genre WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This genre does not exist."}, 400)
                await cursor.execute("DELETE FROM Genre WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeleteGenre:
    return DeleteGenre(app, Method.DELETE, "/genre/delete", JSONResponse)