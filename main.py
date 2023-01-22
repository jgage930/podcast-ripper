from fastapi import FastAPI

from helpers import parse_feed
from database import (
    get_connection,
    insert_episode,
    insert_podcast,
    get_podcast
)


app = FastAPI()


@app.on_event("startup")
def startup_system():
    global podcasts_db
    global episodes_db

    podcasts_db = get_connection("podcasts")
    episodes_db = get_connection("episodes")


@app.post("/podcast/")
def add_podcast(name: str, feed_url: str):
    podcast, episodes = parse_feed(name, feed_url)

    insert_podcast(podcasts_db, podcast)

    for episode in episodes:
        insert_episode(episodes_db, episode)

    return podcast


@app.get("/podcast/{podcast_id}")
def read_podcast(podcast_id: str):
    """Return a single podcast with given id"""
    podcast = get_podcast(podcasts_db, podcast_id)
    return podcast


@app.get("/podcasts")
def read_all_podcasts():
    return podcasts_db.all()


@app.get("/episodes")
def read_all_episodes():
    return episodes_db.all()
