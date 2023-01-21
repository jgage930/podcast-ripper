from fastapi import FastAPI
from tinydb import TinyDB

from helpers import parse_feed

app = FastAPI()


@app.on_event("startup")
def startup_system():
    global db
    db = TinyDB('db.json')


@app.post("/podcast/")
def add_podcast(name: str, feed_url: str):
    # 1.  Parse feed in to objects
    # 2.  Download all podcasts episodes into a folder
    podcast = parse_feed(name, feed_url)

    # convert to json and add to db
    db.insert(podcast.dict())
    return podcast


@app.get("/podcast/{name}")
def read_podcast(name: str):
    pass
