from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class GetPreference(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Preference WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This preference does not exist."}, 400)
                await cursor.execute("SELECT * FROM Preference WHERE id = %s", (id,))
                _, profile_id, genre_id, viewer_guide_id = await cursor.fetchone()
                return JSONResponse({"id": id, "profile_id": profile_id, "genre_id": genre_id, "viewer_guide_id": viewer_guide_id})
            
def setup() -> GetPreference:
    return GetPreference(Method.GET, "/preference/get", JSONResponse)