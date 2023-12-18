import uvicorn
import os

from argparse import ArgumentParser
from dotenv import load_dotenv

from src import App, Connection

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app = App("NetNix", Connection(DB_USER, DB_PASSWORD, "127.0.0.1", 3306, DB_NAME))

for root, _, files in os.walk("endpoints"):
   for file in files:
      if file.endswith(".py"):
        app.addEndpoint(os.path.join(root, file).replace("\\", ".")[:-3])

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("--port", "-p", type=int, default=80)
    args = argparser.parse_args()
    uvicorn.run("app:app", host="0.0.0.0", port=args.port)