from fastapi.responses import JSONResponse
from fastapi import Request

from src import Endpoint, Method, Connection

class GetUsers(Endpoint):
    
    async def callback(self, request: Request) -> JSONResponse:
        if (self.checks.isAuthorized(request.headers.get("token", None), [self.checks.isAdmin])):
            async with Connection() as db:
                async with db.cursor() as cursor:
                    return JSONResponse({})

def setup() -> GetUsers:
    return GetUsers(Method.GET, "/users", JSONResponse)