from typing import Generator
from dataclasses import dataclass
from service.transcript import Match, Transcript
from .youtube_api import ChannelVideos, Video


@dataclass
class SearchResult:
    search_text: str
    video: Video
    matches: list[Match]
    num_results: int

    def json(self):
        return {
            'search_text': self.search_text,
            'video': self.video.json(),
            'matches': [match.json() for match in self.matches],
            'num_results': self.num_results
        }


def search_video(video_id: str, search_text: str) -> SearchResult:
    transcript = Transcript(video_id)
    transcript.process()
    matches = transcript.search(search_text)
    return SearchResult(
        search_text=search_text,
        video=Video(video_id, title='', description='', published_at=''),
        matches=matches,
        num_results=len(matches)
    )


def search_channel(channel_name: str, search_text: str) -> Generator[SearchResult, None, None]:
    channel = ChannelVideos(channel_name)

    while channel.next_page_token:
        for video in channel.videos:
            try:
                found_match = search_video(video.id, search_text)
                if found_match:
                    found_match.video = video
                    yield found_match.json()

            except:
                print('No transcript found')
            # time.sleep(2)
        channel.get_next_page()
