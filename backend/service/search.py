import asyncio
from typing import Generator
from dataclasses import dataclass
from youtube_transcript_api import YouTubeTranscriptApi
from service.transcript import Match, _Transcript, build_transcript, search_transcript
from .youtube_api import ChannelVideos, Video
from db.models.video import Video as DBVideo


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


async def search_video_from_db_or_api(video_id: str, search_text: str) -> SearchResult:
    existing_video = await DBVideo.get_or_none(yt_video_id=video_id)
    if existing_video and existing_video.text_segments:
        transcript = build_transcript(existing_video.text_segments)
        matches = search_transcript(transcript, search_text)
        return SearchResult(
            search_text=search_text,
            video=Video(video_id, title=existing_video.title,
                        description=existing_video.description,
                        published_at=existing_video.published_at,
                        channel_id=existing_video.yt_channel_id),
            matches=matches,
            num_results=len(matches)
        )
    else:
        return search_video(video_id, search_text)


def search_video(video_id: str, search_text: str) -> SearchResult:
    """Search a video for a search text"""
    raw_segments = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = build_transcript(raw_segments)
    matches = search_transcript(transcript, search_text)
    return SearchResult(
        search_text=search_text,
        video=Video(video_id, title='', description='',
                    published_at='', channel_id=''),
        matches=matches,
        num_results=len(matches)
    )


async def search_channel(channel_name: str, search_text: str) -> Generator[SearchResult, None, None]:
    channel = ChannelVideos(channel_name=channel_name)
    await channel.init()

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
        await channel.get_next_page()
