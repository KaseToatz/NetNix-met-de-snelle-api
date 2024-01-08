from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddMovie(Endpoint):

    async def callback(self, title: str = Form(), genre_id: int = Form(), 
                       filepath: str = Form()) -> JSONResponse:
        # get duration and resolution from filepath
        duration = None
        resolution = None

        async with self.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title FROM Movie where movie WHERE title = %s AND duration = %s", (title, duration))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This movie already exists."}, 400)
                await cursor.execute("INSERT INTO Movie(title, duration, genre_id, filepath, resolution) VALUES(%s, %s, %s, %s, %s)", (title, duration, genre_id, filepath, resolution))
                return JSONResponse({})
            
def setup(app : App) -> AddMovie:
    return AddMovie(app, Method.POST, "/movie/add", JSONResponse)
