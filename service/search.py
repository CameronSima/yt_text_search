import time
from dataclasses import dataclass
from service.transcript import Match, Transcript
from .youtube_api import ChannelVideos, Video


@dataclass
class SearchResult:
    search_text: str
    video: Video
    matches: list[Match]
    num_results: int


def search_video(video_id: str, search_text: str) -> SearchResult:
    transcript = Transcript(video_id)
    transcript.process()
    matches = transcript.search(search_text)
    return SearchResult(
        search_text=search_text,
        video=Video(video_id),
        matches=matches,
        num_results=len(matches)
    )


def search_channel(channel_name: str, search_text: str) -> list[SearchResult]:
    channel = ChannelVideos(channel_name)
    results = []
    while channel.next_page_token:
        for video in channel.videos:
            print(video.title, video.id)
            try:
                found_match = search_video(video.id, search_text)
                if found_match:
                    results.append(found_match)
            except:
                print('No transcript found')
            time.sleep(2)
        channel.get_next_page()
    return results
