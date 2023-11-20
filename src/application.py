from fastapi import FastAPI
from importlib import import_module
from .exceptions import MissingSetupFunction

class App(FastAPI):

    def __init__(self, title: str) -> None:
        super().__init__(title=title, redoc_url=None, swagger_ui_oauth2_redirect_url=None)

    def loadEndpoint(self, path: str) -> None:
        module = import_module(path)
        try:
            endpoint = module.setup(self)
            self.add_api_route(endpoint.path, endpoint.callback, response_class=endpoint.responseClass, methods=[endpoint.method.name])
        except:
            raise MissingSetupFunction