from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeletePrefrence(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Prefrence WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This prefrence does not exist."}, 400)
                await cursor.execute("DELETE FROM Prefrence WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeletePrefrence:
    return DeletePrefrence(app, Method.DELETE, "/prefrence/delete", JSONResponse)