from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class AddViewerGuide(Endpoint):

    async def callback(self, description: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT * FROM ViewerGuide WHERE description = %s", (description,))
                if await cursor.fetchone():
                    return JSONResponse({"error": "This viewer guide already exists."}, 400)
                await cursor.execute("INSERT INTO ViewerGuide(description) VALUES(%s)", (description))
                return JSONResponse({})
            
def setup(app : App) -> AddViewerGuide:
    return AddViewerGuide(app, Method.POST, "/viewerGuide/add", JSONResponse)