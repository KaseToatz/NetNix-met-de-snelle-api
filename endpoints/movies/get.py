from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetMovie(Endpoint):

    async def callback(self, id: int = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id, title FROM Movie")
                movies = await cursor.fetchall()
                if not movies:
                    return JSONResponse({"error": "There aren't any movies yet."}, 400)
                movies_list = [{"id": movie[0], "title": movie[1]} for movie in movies]
                return JSONResponse({movies_list})
            
def setup(app : App) -> GetMovie:
    return GetMovie(app, Method.GET, "/movies/get", JSONResponse)