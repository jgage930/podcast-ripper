from tinydb import TinyDB
from models import Podcast, Episode


def get_connection(table_name: str) -> TinyDB:
    db = None
    match table_name:
        case "podcasts":
            db = TinyDB("podcasts.json")
        case "episodes":
            db = TinyDB("episodes.json")
        case _:
            raise(ValueError(f"No Table Named {table_name}"))

    return db


def insert_podcast(db: TinyDB, podcast: Podcast):
    db.insert(podcast.dict())


def insert_episode(db: TinyDB, episode: Episode):
    db.insert(episode.dict())
