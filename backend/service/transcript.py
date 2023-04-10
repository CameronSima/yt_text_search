import math
from typing import TypedDict
from dataclasses import dataclass
from youtube_transcript_api import YouTubeTranscriptApi
from service.utils import get_matched_indexes, format_time


@dataclass
class TextSegment:
    id: str
    i_start: int
    i_end: int
    text: str
    original_text: str
    start: float
    duration: float
    text_preceding: list[str]
    text_following: list[str]

    def start_rounded(self):
        return math.floor(self.start)

    def end_rounded(self):
        return math.floor(self.start + self.duration)


@dataclass
class Match:
    id: str
    preceding_text: str
    exact_text: str
    following_text: str
    start_seconds: int
    end_seconds: int

    def json(self):
        return {
            'id': self.id,
            'preceding_text': self.preceding_text,
            'exact_text': self.exact_text,
            'following_text': self.following_text,
            'start_seconds': self.start_seconds,
            'end_seconds': self.end_seconds,
            'start_seconds_formatted': format_time(self.start_seconds),
            'end_seconds_formatted': format_time(self.end_seconds),
        }


def build_match(search_text: str, segments: list[TextSegment]) -> Match:
    """Split text into preceding, exact matching, and following"""
    first_segment = segments[0]
    last_segment = segments[-1]
    preceding_text = ''.join(first_segment.text_preceding).strip()
    following_text = ''.join(last_segment.text_following).strip()
    main_text_lower = ''.join([x.text for x in segments]).strip()
    main_text_original = ''.join(
        [x.original_text for x in segments]).strip()
    full_text = preceding_text + ' ' + main_text_lower + ' ' + following_text
    full_text_original = preceding_text + ' ' + \
        main_text_original + ' ' + following_text

    # find indexes of the search text in the full text, with lowercase matching
    indexes = get_matched_indexes(full_text, search_text.lower())

    # split the text into preceding, exact matching, and following from
    # the original text
    preceding = full_text_original[:indexes[0][0]]
    exact = full_text_original[indexes[0][0]:indexes[0][1]]
    following = full_text_original[indexes[0][1]:]

    return Match(
        id=first_segment.id,
        preceding_text=preceding.strip(),
        exact_text=exact.strip(),
        following_text=following.strip(),

        # add a 2 second buffer as lead in
        start_seconds=first_segment.start_rounded() - 2,
        end_seconds=last_segment.end_rounded(),
    )


class Transcript:
    video_id: str
    segments: list[TextSegment]
    full_text: str
    transcript_segments: list[dict]
    _raw_transcript: list[dict]

    def __init__(self, video_id):
        self.segments = []
        self.full_text = ''
        self.video_id = video_id
        self._fetch_transcript()

    def _fetch_transcript(self):
        try:
            self._raw_transcript = YouTubeTranscriptApi.get_transcript(
                self.video_id)
        except:
            self._raw_transcript = []

    def process(self):
        num_bookends = 1
        char_index = 0

        num_segments = len(self._raw_transcript)
        for i, segment in enumerate(self._raw_transcript):

            # add space to preserve word boundaries
            text = segment['text'] + ' '
            i_end = char_index + len(text)
            segment_obj = TextSegment(
                id=i,
                text=text.lower(),
                original_text=text,
                start=segment['start'],
                duration=segment['duration'],
                i_start=char_index,
                i_end=i_end,
                text_preceding=[],
                text_following=[],
            )

            # add some text on either end of the matching text
            # for context
            if i >= num_bookends:
                preceding = self._raw_transcript[i - num_bookends: i]
                segment_obj.text_preceding += [x['text'] for x in preceding]
            if i < num_segments - num_bookends:
                following = self._raw_transcript[i + 1: i + num_bookends + 1]
                segment_obj.text_following += [x['text'] for x in following]

            self.segments.append(segment_obj)
            self.full_text += segment_obj.text
            char_index = i_end

    def search(self, text: str) -> list[Match]:
        """Search for text in the transcript, returning a list of matches."""
        matches: list[Match] = []
        indexes = get_matched_indexes(self.full_text, text.lower())

        for i_start, i_end in indexes:
            matching_segments = []
            for segment in self.segments:
                if segment.i_end == i_start:
                    i_start += 1
                if segment.i_start <= i_start <= segment.i_end or \
                        segment.i_start <= i_end <= segment.i_end:
                    matching_segments.append(segment)
            match = build_match(text, matching_segments)
            matches.append(match)
        return matches


# class RawSegment(TypedDict):
#     start: float
#     duration: float
#     text: str


# def build_segments(raw_segments: list[RawSegment], num_bookends=1) -> dict:
#     segments = []
#     full_text = ''
#     char_index = 0

#     num_segments = len(raw_segments)
#     for i, segment in enumerate(raw_segments):

#         # add space to preserve word boundaries
#         text = segment['text'] + ' '
#         i_end = char_index + len(text)
#         segment_obj = TextSegment(
#             id=i,
#             text=text.lower(),
#             original_text=text,
#             start=segment['start'],
#             duration=segment['duration'],
#             i_start=char_index,
#             i_end=i_end,
#             text_preceding=[],
#             text_following=[],
#         )

#         # add some text on either end of the matching text
#         # for context
#         if i >= num_bookends:
#             preceding = raw_segments[i - num_bookends: i]
#             segment_obj.text_preceding += [x['text'] for x in preceding]
#         if i < num_segments - num_bookends:
#             following = raw_segments[i + 1: i + num_bookends + 1]
#             segment_obj.text_following += [x['text'] for x in following]

#         segments.append(segment_obj)
#         full_text += segment_obj.text
#         char_index = i_end

#     return {
#         'segments': segments,
#         'full_text': full_text,
#     }
