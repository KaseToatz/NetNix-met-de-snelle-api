from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetPrefrence(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Prefrence WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This prefrence does not exist."}, 400)
                await cursor.execute("SELECT * FROM Prefrence WHERE id = %s", (id,))
                _, profile_id, genre_id, viewer_guide_id = await cursor.fetchone()
                return JSONResponse({"id": id, "profile_id": profile_id, "genre_id": genre_id, "viewer_guide_id": viewer_guide_id})
            
def setup(app : App) -> GetPrefrence:
    return GetPrefrence(app, Method.GET, "/prefrence/get", JSONResponse)