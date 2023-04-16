from youtube_transcript_api import YouTubeTranscriptApi
from db.models.video import Video, yt_video_to_video
from service.youtube_api import ChannelVideos


async def save_videos_from_channel(channel: ChannelVideos, db_videos: list[Video]):
    api_videos = [yt_video_to_video(video) async for video in channel.videos_generator()]
    unsaved_videos = [video for video in api_videos if video not in db_videos]

    for video in unsaved_videos:
        try:
            video.segments = YouTubeTranscriptApi.get_transcript(
                video.yt_video_id)
        except Exception as e:
            print(e)
            video.segments = []

    await Video.bulk_create(unsaved_videos, ignore_conflicts=True)
