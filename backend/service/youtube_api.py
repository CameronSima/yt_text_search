from dataclasses import dataclass
import requests

from service.transcript import TextSegment

API_KEY = "AIzaSyBDHVhZFnS3BR7VvB2k32rGbZHHF8NO38s"
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


def get_channel_id(username):
    url = f"https://www.googleapis.com/youtube/v3/channels?key={API_KEY}&forUsername={username}&part=id"
    response = requests.get(url)
    data = response.json()
    return data['items'][0]['id']


def _get_channel_playlist_id(channel_name: str) -> list[dict]:
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername={channel_name}&key={API_KEY}"
    response = requests.get(url)
    data_json = response.json()
    print(data_json)
    data = data_json['items']
    return data[0]['contentDetails']['relatedPlaylists']['uploads']


def _get_videos(playlists_id: str, page_token: str or None) -> tuple[list[dict], str]:
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={MAX_RESULTS}&playlistId={playlists_id}&key={API_KEY}"

    if page_token:
        url += f"&pageToken={page_token}"

    response = requests.get(url)
    return response.json()


class ChannelVideos:
    channel_name: str
    channel_playlist_id: str
    next_page_token: str
    videos: list[Video]

    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.next_page_token = None
        self.channel_playlist_id = _get_channel_playlist_id(self.channel_name)
        self.videos = self.get_channel_videos()

    def get_next_page(self) -> list[Video]:
        new_vids = self.get_channel_videos(self.next_page_token)
        self.videos = new_vids

    def get_channel_videos(self, page_token=None) -> tuple[list[Video], str]:
        videos_json = _get_videos(self.channel_playlist_id, page_token)
        self.next_page_token = videos_json.get('nextPageToken')
        videos = videos_json.get('items')

        return [Video(
            title=video['snippet']['title'],
            published_at=video['snippet']['publishedAt'],
            description=video['snippet']['description'],
            id=video['snippet']['resourceId']['videoId']
        ) for video in videos]


print(get_channel_id('proguide66'))
