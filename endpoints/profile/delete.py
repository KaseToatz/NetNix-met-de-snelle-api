from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeleteProfile(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Profile WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This profile does not exist."}, 400)
                await cursor.execute("DELETE FROM Profile WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeleteProfile:
    return DeleteProfile(app, Method.DELETE, "/profile/delete", JSONResponse)