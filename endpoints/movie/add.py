from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddMovie(Endpoint):

    async def callback(self, title: str = Form(), durration: int = Form(), genre_id: int = Form(), 
                       filepath: str = Form(), resolution: str = Form()) -> JSONResponse:
        async with self.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT title FROM Movie where movie WHERE title = %s AND durration = %i", (title, durration,))
                title = await cursor.fetchone()
                durration = await cursor.fetchone()
                if title & durration:
                    return JSONResponse({"error": "This movie already exists."}, 400)
                await cursor.execute("INSERT INTO Movie(title, durration, genre_id, filepath, resolution) VALUES(%s, %i, %i, %s, %s)", (title, durration, genre_id, filepath, resolution))
                return JSONResponse({})
            
def setup(app : App) -> AddMovie:
    return AddMovie(app, Method.POST, "/movie/add", JSONResponse)
