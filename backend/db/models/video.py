from tortoise.models import Model
from tortoise import fields
from service.youtube_api import Video as YTVideo


class Video(Model):
    id = fields.IntField(pk=True)
    yt_video_id = fields.CharField(max_length=255, index=True)
    yt_channel_id = fields.CharField(max_length=255, index=True)
    title = fields.CharField(max_length=999, index=True)
    url = fields.CharField(max_length=255)
    published_at = fields.DatetimeField(auto_now_add=True)
    text_segments = fields.JSONField()

    class Meta:
        table = 'video'

    def __str__(self):
        return self.title

    def __eq__(self, other: object) -> bool:
        return self.yt_video_id == other.yt_video_id


def yt_video_to_video(yt_video: YTVideo):
    return Video(
        yt_video_id=yt_video.id,
        yt_channel_id=yt_video.channel_id,
        title=yt_video.title,
        url=yt_video.url(),
        published_at=yt_video.published_at,
    )


async def create_from_yt_api(video: YTVideo):
    if not await Video.exists(yt_video_id=video.id):
        return await Video.create(
            yt_video_id=video.id,
            yt_channel_id=video.channel_id,
            title=video.title,
            url=video.url(),
            published_at=video.published_at,
        )
