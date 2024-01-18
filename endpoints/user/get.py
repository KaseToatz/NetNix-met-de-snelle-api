from fastapi.responses import JSONResponse
from fastapi import Request

from src import App, Endpoint, Method, isAuthorized

class GetUsers(Endpoint):
    
    async def callback(self, request: Request) -> JSONResponse:
        if (isAuthorized(request.headers.get("token", None), lambda email: email is not None)):
            async with self.app.pool.acquire() as db:
                async with db.cursor() as cursor:
                    return JSONResponse({})

def setup(app: App) -> GetUsers:
    return GetUsers(app, Method.GET, "/users", JSONResponse)