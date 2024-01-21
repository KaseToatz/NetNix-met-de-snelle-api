from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class DeletePreference(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id FROM Preference WHERE id = %s", (id,))
                if not await cursor.fetchone():
                    return JSONResponse({"error": "This preference does not exist."}, 400)
                await cursor.execute("DELETE FROM Preference WHERE id = %s", (id,))
                return JSONResponse({})
            
def setup() -> DeletePreference:
    return DeletePreference(Method.DELETE, "/preference/delete", JSONResponse)