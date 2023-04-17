import asyncio
import functools
from huey import RedisHuey
from fastapi import FastAPI
from constants import REDIS_CONNECTION_STRING
from youtube_transcript_api import YouTubeTranscriptApi
from db.models.video import Video, yt_video_to_video
from service.youtube_api import ChannelVideos
from init_db import init

print(REDIS_CONNECTION_STRING)

# redis://yt_text_search:Simc1o0q!@redis-13173.c10.us-east-1-2.ec2.cloud.redislabs.com:13173
huey = RedisHuey('my-app', url=REDIS_CONNECTION_STRING)


def run_async_task(func):
    """Huey can't run async functions, so this wrapper is needed"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_forever()
        loop.run_until_complete(func(*args, **kwargs))
    return wrapper


@huey.task()
@run_async_task
async def save_videos(channel: ChannelVideos, db_videos: list[Video]):
    await init()
    print("Task called")
    api_videos = []
    async for video in channel.videos_generator():
        api_videos.append(yt_video_to_video(video))

    unsaved_videos = [video for video in api_videos if video not in db_videos]
    print(unsaved_videos)

    for video in unsaved_videos:
        print(video)
        try:

            video.segments = YouTubeTranscriptApi.get_transcript(
                video.yt_video_id)
            print("Got segments")
        except Exception as e:
            print(e)
            video.segments = []

    await Video.bulk_create(unsaved_videos, ignore_conflicts=True)
    return unsaved_videos


@huey.task()
def test_task():
    print("Test task called")
    return "Return value"
