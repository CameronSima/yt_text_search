from tortoise.models import Model
from tortoise import fields


class Video(Model):
    id = fields.IntField(pk=True)
    yt_video_id = fields.CharField(max_length=255)
    yt_channel_id = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)
    published_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'video'

    def __str__(self):
        return self.title
