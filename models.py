from pydantic import BaseModel


class Episode(BaseModel):
    title: str
    summary: str
    author: str
    image_link: str
    audio_link: str
    published_date: str


class Podcast(BaseModel):
    title: str
    feed_url: str
    episodes: list[Episode]
    last_updated: str
