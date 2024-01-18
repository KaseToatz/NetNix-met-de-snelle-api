from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class DeleteSubtitle(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Subtitle WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This subtitle does not exist."}, 400)
                await cursor.execute("DELETE FROM subtitle WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup(app : App) -> DeleteSubtitle:
    return DeleteSubtitle(app, Method.DELETE, "/subtitle/delete", JSONResponse)