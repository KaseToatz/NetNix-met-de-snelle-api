from fastapi.responses import PlainTextResponse

from src import App, Endpoint, Method

class Template(Endpoint):
    
    async def callback(self) -> PlainTextResponse:
        return "Hello World!"

def setup(app: App) -> Template:
    return Template(app, Method.GET, "/", PlainTextResponse)