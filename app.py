import uvicorn

from fastapi import FastAPI
from argparse import ArgumentParser

app = FastAPI(title="NetNix API", redoc_url=None, swagger_ui_oauth2_redirect_url=None)

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--port", "-p", type=int, default=80)
    args = argparser.parse_args()
    uvicorn.run("app:app", host="0.0.0.0", port=args.port)