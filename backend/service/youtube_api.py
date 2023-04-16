from dataclasses import dataclass
import service.http_client as http_client
import re

from service.transcript import TextSegment
from constants import YOUTUBE_API_KEY

MAX_RESULTS = 50


@dataclass
class Video:
    id: str
    channel_id: str
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
        }


@dataclass
class Channel:
    id: str
    title: str
    identifier: str
    description: str
    published_at: str

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'published_at': self.published_at,
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


def get_playlist_id_from_channel_id(channel_id: str) -> str:
    """Replace UC with UU to get the uploads playlist id"""
    return channel_id.replace('UC', 'UU')


async def get_playlist_id_from_channel_name(channel_name: str) -> list[dict]:
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername={channel_name}&key={YOUTUBE_API_KEY}"
    response = await http_client.get(url)
    data_json = response.json()
    print(data_json)
    data = data_json['items']
    return data[0]['contentDetails']['relatedPlaylists']['uploads']


async def get_videos_from_playlist_id(playlists_id: str, page_token: str or None) -> dict:
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={MAX_RESULTS}&playlistId={playlists_id}&key={YOUTUBE_API_KEY}"

    if page_token:
        url += f"&pageToken={page_token}"

    response = await http_client.get(url)
    data_json = response.json()
    data = data_json['items']

    def map_video(video) -> Video:
        return Video(
            id=video['snippet']['resourceId']['videoId'],
            title=video['snippet']['title'],
            description=video['snippet']['description'],
            published_at=video['snippet']['publishedAt'],
            channel_id=video['snippet']['channelId'],
        )

    videos = [map_video(video) for video in data]

    # videos = []
    # for video in data:
    #     videos.append(
    #         Video(
    #             id=video['id'],
    #             title=video['snippet']['title'],
    #             description=video['snippet']['description'],
    #             published_at=video['snippet']['publishedAt'],
    #             channel_id=video['snippet']['channelId'],
    #         ))

    return {
        'videos': videos,
        'pagedResults': len(videos),
        'totalResults': data_json.get('pageInfo', {}).get('totalResults', 0),
        'nextPageToken': data_json.get('nextPageToken', None),
    }


async def search_channels(search_text: str) -> list[Channel]:
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&maxResults=10&q={search_text}&key={YOUTUBE_API_KEY}'
    response = await http_client.get(url)
    data_json = response.json()
    data = data_json['items']
    return [Channel(
        title=channel['snippet']['title'],
        published_at=channel['snippet']['publishedAt'],
        description=channel['snippet']['description'],
        id=channel['snippet']['channelId']
    ) for channel in data]


class ChannelVideos:
    channel_name: str
    channel_id: str
    channel_playlist_id: str
    next_page_token: str
    total_channel_videos: int
    videos: list[Video]

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.next_page_token = None

    async def init(self):
        self.channel_playlist_id = get_playlist_id_from_channel_id(
            self.channel_id)
        self.videos = await self.get_channel_videos()

    async def videos_generator(self):
        while self.next_page_token:
            for video in self.videos:
                yield video
            await self.get_next_page()

    async def get_next_page(self) -> list[Video]:
        new_vids = await self.get_channel_videos(self.next_page_token)
        self.videos = new_vids

    async def get_channel_videos(self, page_token=None) -> tuple[list[Video], str]:
        results = await get_videos_from_playlist_id(self.channel_playlist_id, page_token)
        self.next_page_token = results.get('nextPageToken')
        self.total_channel_videos = results.get('totalResults')
        return results.get('videos')
