from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeleteSerie(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Movie WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This serie does not exist."}, 400)
                await cursor.execute("DELETE FROM Serie WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeleteSerie:
    return DeleteSerie(app, Method.DELETE, "/serie/delete", JSONResponse)