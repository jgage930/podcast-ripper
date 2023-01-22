import feedparser
import os
import os.path
from datetime import datetime
from models import Podcast, Episode
import requests
import uuid


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

        media_content = entry.get("media_content")
        image_link = ""
        audio_link = ""
        for content in media_content:
            if content.get('type') == "audio/mpeg":
                audio_link = content.get('url')

            if content.get('type') == "image/jpeg":
                image_link = content.get('url')

        episode = Episode(
            id=str(uuid.uuid4()),
            title=title,
            summary=summary,
            author=author,
            image_link=image_link,
            audio_link=audio_link,
            published_date=published_date,
            podcast_id=podcast_id
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


def download_episodes(podcast: Podcast) -> str:
    # downloads episodes to a folder named the podcast title
    directory = "podcasts"
    folders = [dir_name for dir_name in os.listdir(
        directory) if os.path.isdir(f"podcasts/{dir_name}")]

    if podcast.title not in folders:
        os.mkdir(f"podcasts/{podcast.title}")

    episodes_directory = f"podcasts/{podcast.title}"
    os.chdir(episodes_directory)

    for episode in podcast.episodes:
        response = requests.get(episode.audio_link)
        episode_name = to_snake_case(episode.title)
        with open(f"{episode_name}.mp3", 'wb') as file:
            file.write(response.content)
