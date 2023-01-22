from pydantic import BaseModel


class Episode(BaseModel):
    id: str
    title: str
    summary: str
    author: str
    image_link: str
    audio_link: str
    published_date: str
    podcast_id: str


class Podcast(BaseModel):
    id: str
    title: str
    feed_url: str
    last_updated: str
