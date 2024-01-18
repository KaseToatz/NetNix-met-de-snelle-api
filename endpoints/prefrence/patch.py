from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchPrefrence(Endpoint):

    async def callback(self, id: int = Form(), profile_id: int = Form(), genre_id: int = Form(), viewer_guide_list: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT description FROM Prefrence WHERE id = %s", (id,))
                prefrence = await cursor.fetchone()
                if not prefrence:
                    return JSONResponse({"error": "This prefrence does not exist."}, 400)
                dbprofile_id, dbgenre_id, dbviewer_guide_liste = await cursor.fetchone() 
                await cursor.execute("UPDATE Prefrence SET description = %s WHERE id = %s", (prefrence or dbprofile_id, genre_id or dbgenre_id, viewer_guide_list or dbviewer_guide_liste, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchPrefrence:
    return PatchPrefrence(app, Method.PATCH, "/prefrence/patch", JSONResponse)