from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchViewerGuide(Endpoint):

    async def callback(self, id: int = Form(), description: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM ViewerGuide WHERE id = %s", (id,))
                viewerGuide = await cursor.fetchone()
                if not viewerGuide:
                    return JSONResponse({"error": "This viewer guide does not exist."}, 400)
                dbdescription = await cursor.fetchone() 
                await cursor.execute("UPDATE ViewerGuide SET description = %s WHERE id = %s", (description or dbdescription, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchViewerGuide:
    return PatchViewerGuide(app, Method.PATCH, "/viewerGuide/patch", JSONResponse)