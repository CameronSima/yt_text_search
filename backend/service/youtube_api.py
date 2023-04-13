from dataclasses import dataclass
import service.http_client as http_client
import re

from service.transcript import TextSegment
from constants import YOUTUBE_API_KEY

MAX_RESULTS = 50


@dataclass
class Video:
    id: str
    title: str
    description: str
    published_at: str

    def url(self):
        return f"https://www.youtube.com/watch?v={self.id}"

    def segment_url(self, segment: TextSegment):
        return f"https://www.youtube.com/embed/{self.id}?start={segment.start_rounded()}"

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at,
            'url': self.url(),
        }


async def get_channel_id(username):
    if username.startswith('@'):
        username = username[1:]

    url = f"https://www.youtube.com/@{username}"
    page_source = await http_client.get(url).text
    match = re.search(r'"externalId":"([\w-]+)"', page_source)

    if match:
        external_id = match.group(1)
        print(external_id)
    else:
        print('External ID not found')


async def _get_channel_playlist_id(channel_name: str) -> list[dict]:
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername={channel_name}&key={YOUTUBE_API_KEY}"
    response = await http_client.get(url)
    data_json = response.json()
    print(data_json)
    data = data_json['items']
    return data[0]['contentDetails']['relatedPlaylists']['uploads']


async def _get_videos(playlists_id: str, page_token: str or None) -> tuple[list[dict], str]:
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={MAX_RESULTS}&playlistId={playlists_id}&key={YOUTUBE_API_KEY}"

    if page_token:
        url += f"&pageToken={page_token}"

    response = await http_client.get(url)
    return response.json()


async def search_channels(search_text: str) -> list[Video]:
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&maxResults=10&q={search_text}&key={YOUTUBE_API_KEY}'
    response = await http_client.get(url)
    data_json = response.json()
    data = data_json['items']
    return [Video(
        title=channel['snippet']['title'],
        published_at=channel['snippet']['publishedAt'],
        description=channel['snippet']['description'],
        id=channel['snippet']['channelId']
    ) for channel in data]


class ChannelVideos:
    channel_name: str
    channel_playlist_id: str
    next_page_token: str
    videos: list[Video]

    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.next_page_token = None

    async def init(self):
        self.channel_playlist_id = await _get_channel_playlist_id(self.channel_name)
        self.videos = await self.get_channel_videos()

    async def get_next_page(self) -> list[Video]:
        new_vids = await self.get_channel_videos(self.next_page_token)
        self.videos = new_vids

    async def get_channel_videos(self, page_token=None) -> tuple[list[Video], str]:
        videos_json = await _get_videos(self.channel_playlist_id, page_token)
        self.next_page_token = videos_json.get('nextPageToken')
        videos = videos_json.get('items')

        return [Video(
            title=video['snippet']['title'],
            published_at=video['snippet']['publishedAt'],
            description=video['snippet']['description'],
            id=video['snippet']['resourceId']['videoId']
        ) for video in videos]
