import re
from datetime import timedelta


def get_matched_indexes(text, search_text) -> list[tuple[int, int]]:
    """Return a list of start and end indexes where the search text is found in the text"""
    return [(m.start(), m.end()) for m in re.finditer(search_text, text)]


def format_time(time):
    formatted = str(timedelta(seconds=time))
    # remove ms
    return formatted.split('.')[0]


def clean_video_id(video_id_or_url) -> str:
    """Return a video id from a video id or a video url"""
    youtube_urls = [
        'https://www.youtube.com/watch?v=',
        'https://youtu.be/',
        'https://www.youtube.com/embed/',
    ]
    for url in youtube_urls:
        if video_id_or_url.startswith(url):
            return video_id_or_url.replace(url, '')

    return video_id_or_url


def clean_channel_name(channel_name: str) -> str:
    """Return a channel name from a channel name or a channel url"""
    youtube_urls = [
        'https://www.youtube.com/channel/',
        'https://www.youtube.com/c/',
    ]
    for url in youtube_urls:
        if channel_name.startswith(url):
            return channel_name.replace(url, '')

    # strip @ from channel name
    if channel_name.startswith('@'):
        channel_name = channel_name[1:]

    return channel_name
