from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetAllSeries(Endpoint):

    async def callback(self,) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id, title FROM Serie")
                series = await cursor.fetchall()
                if not series:
                    return JSONResponse({"error": "There aren't any series yet."}, 400)
                serie_list = [{"id": serie[0], "title": serie[1]} for serie in series]
                return JSONResponse({serie_list})
            
def setup(app : App) -> GetAllSeries:
    return GetAllSeries(app, Method.GET, "/serie/getAll", JSONResponse)