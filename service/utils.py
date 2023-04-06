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
