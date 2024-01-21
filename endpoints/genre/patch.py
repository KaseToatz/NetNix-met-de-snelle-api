from fastapi.responses import JSONResponse
from fastapi import Form

from src import Endpoint, Method

class PatchGenre(Endpoint):

    async def callback(self, id: int = Form(), description: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT description FROM Genre WHERE id = %s", (id,))
                genre = await cursor.fetchone()
                if not genre:
                    return JSONResponse({"error": "This genre does not exist."}, 400)
                dbdescription = await cursor.fetchone() 
                await cursor.execute("UPDATE Genre SET description = %s WHERE id = %s", (description or dbdescription, id))
                return JSONResponse({})
            
def setup() -> PatchGenre:
    return PatchGenre(Method.PATCH, "/serie/patch", JSONResponse)