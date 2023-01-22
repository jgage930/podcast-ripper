from fastapi import FastAPI

from helpers import parse_feed, download_episode
from database import (
    get_connection,
    insert_episode,
    insert_podcast,
    get_podcast,
    get_episode,
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
def get_podcast_by_id(podcast_id: str):
    """Return a single podcast with given id"""
    podcast = get_podcast(podcasts_db, podcast_id)
    return podcast


@app.get("/podcasts")
def get_all_podcasts():
    return podcasts_db.all()


@app.get("/episode/{episode_id}")
def get_episode_by_id(episode_id: str):
    episode = get_episode(episodes_db, episode_id)
    return episode


@app.get("/episodes")
def get_all_episodes():
    return episodes_db.all()


@app.post("/download/episode/{episode_id}")
def download_episode_by_id(episode_id: str):
    try:
        download_episode(episodes_db, episode_id)
    except Exception as e:
        return {'msg': f"Could not download podcast.  {e}"}

    return {'msg': f"Downloaded {episode_id}"}
