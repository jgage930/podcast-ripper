import feedparser
import os
import os.path
from datetime import datetime
from models import Podcast, Episode
from database import get_episode, update_downloaded
import requests
import uuid
from typing import Any, Union
from tinydb import TinyDB


def to_datetime(date_str: str) -> datetime:
    plus_index = date_str.find("+")
    minus_index = date_str.find("-")

    if plus_index != -1:
        date_str = date_str[:plus_index]

    if minus_index != -1:
        date_str = date_str[:minus_index]

    return datetime.strptime(
        date_str.strip(),
        "%a, %d %b %Y %H:%M:%S"
    )


def parse_audio_link(entry: dict[str: Any]) -> Union[str, None]:
    audio_link = None

    links: list[dict] = entry.get("links")

    for link in links:
        if "audio" in link.get("type"):
            audio_link = link.get("href")

    return audio_link


def parse_feed(name: str, feed_url: str) -> tuple[Podcast, list[Episode]]:
    # parse feed into objects
    episodes: list[Episode] = []

    feed = feedparser.parse(feed_url)

    entries = feed['entries']

    podcast_id = str(uuid.uuid4())

    for entry in entries:

        title = entry.get("title")
        summary = entry.get("summary")
        author = entry.get("author")
        published_date = entry.get("published")
        audio_link = parse_audio_link(entry)

        episode = Episode(
            id=str(uuid.uuid4()),
            title=title,
            summary=summary,
            author=author,
            audio_link=audio_link,
            published_date=published_date,
            podcast_id=podcast_id,
        )

        episodes.append(episode)

    now = datetime.now()
    now_str = now.strftime("%m-%d-%Y %H:%M:%S")

    podcast = Podcast(
        id=podcast_id,
        title=name,
        feed_url=feed_url,
        episodes=episodes,
        last_updated=now_str
    )

    return podcast, episodes


def to_snake_case(text: str) -> str:
    lower = text.lower()
    return lower.replace(" ", "_")


def download_episode(episode_db: TinyDB, episode_id: str):
    # download an episode based on episode_id
    episode: Episode = get_episode(episode_db, episode_id)

    link = episode.audio_link
    id = episode.id
    response = requests.get(link)

    os.chdir("podcasts")
    with open(f"{id}.mp3", "wb") as audio_file:
        audio_file.write(response.content)

    update_downloaded(episode_db, episode_id, True)
