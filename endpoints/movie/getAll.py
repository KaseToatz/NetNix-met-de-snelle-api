from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class GetAllMovies(Endpoint):

    async def callback(self) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT id, title FROM Movie")
                movies = await cursor.fetchall()
                if not movies:
                    return JSONResponse({"error": "There aren't any movies yet."}, 400)
                movie_list = [{"id": movie[0], "title": movie[1]} for movie in movies]
                return JSONResponse(movie_list)
            
def setup(app : App) -> GetAllMovies:
    return GetAllMovies(app, Method.GET, "/movie/getAll", JSONResponse)