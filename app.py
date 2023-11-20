import uvicorn

from argparse import ArgumentParser

from src import App, Connection

DB_USER = ""
DB_PASSWORD = ""
DB_NAME = ""

app = App("NetNix", Connection(DB_USER, DB_PASSWORD, "127.0.0.1", 3306, DB_NAME))

app.addEndpoint("endpoints.template")

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--port", "-p", type=int, default=80)
    args = argparser.parse_args()
    uvicorn.run("app:app", host="0.0.0.0", port=args.port)