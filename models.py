from pydantic import BaseModel


class Episode(BaseModel):
    id: str
    title: str
    summary: str
    author: str
    audio_link: str
    published_date: str
    podcast_id: str
    downloaded: bool = False


class Podcast(BaseModel):
    id: str
    title: str
    feed_url: str
    last_updated: str
