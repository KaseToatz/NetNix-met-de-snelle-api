from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchSerie(Endpoint):

    async def callback(self, id: int = Form(), title: str = Form(), genre_id: int = Form(), resolution: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title, genre_id, resolution FROM Serie WHERE id = %s", (id,))
                serie = await cursor.fetchone()
                if not serie:
                    return JSONResponse({"error": "This serie does not exist."}, 400)
                dbtitle, dbgenre_id, dbresolution = await cursor.fetchone() 
                await cursor.execute("UPDATE Serie SET title = %s, genre_id = %s, resolution = %s WHERE id = %s", (title or dbtitle, genre_id or dbgenre_id, resolution or dbresolution, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchSerie:
    return PatchSerie(app, Method.PATCH, "/serie/patch", JSONResponse)