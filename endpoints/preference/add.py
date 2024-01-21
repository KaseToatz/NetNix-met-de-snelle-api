from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class AddPreference(Endpoint):

    async def callback(self, profile_id: int = Form(), genre_id: int = Form(), viewer_guide_id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM Profile WHERE id = %s", (profile_id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This profile does not exist."}, 400)
                await cursor.execute("INSERT INTO Preference(profile_id, genre_id, viewer_guide_id) VALUES(%s)", (profile_id, genre_id, viewer_guide_id))
                return JSONResponse({})
            
def setup() -> AddPreference:
    return AddPreference(Method.POST, "/preference/add", JSONResponse)