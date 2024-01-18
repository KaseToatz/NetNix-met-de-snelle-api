from fastapi.responses import JSONResponse
from fastapi import Form

from src import App, Endpoint, Method

class PatchProfile(Endpoint):

    async def callback(self, id: int = Form(), name: str = Form(), age: int = Form(), image_filepath: str = Form, language: str = Form()) -> JSONResponse:

        async with self.app.pool.acquire() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT name, age, image_filepath, language resolution FROM Profile WHERE id = %s", (id,))
                profile = await cursor.fetchone()
                if not profile:
                    return JSONResponse({"error": "This profile does not exist."}, 400)
                dbname, dbage, dbimage_filepath, dblanguage = await cursor.fetchone() 
                await cursor.execute("UPDATE Profile SET name = %s, age = %s, image_filepath = %s, language = %s WHERE id = %s", (name or dbname, age or dbage, image_filepath or dbimage_filepath, language or dblanguage, id))
                return JSONResponse({})
            
def setup(app : App) -> PatchProfile:
    return PatchProfile(app, Method.PATCH, "/profile/patch", JSONResponse)