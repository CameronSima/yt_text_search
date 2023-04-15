from typing import TypedDict
from dataclasses import dataclass
from service.match import Match, build_match
from service.text_segment import TextSegment
from service.utils import get_matched_indexes


@dataclass
class _Transcript:
    full_text: str
    segments: list[TextSegment]


class RawSegment(TypedDict):
    start: float
    duration: float
    text: str


def build_transcript(raw_segments: list[RawSegment], num_bookends=1) -> _Transcript:
    segments = []
    full_text = ''
    char_index = 0

    num_segments = len(raw_segments)
    for i, segment in enumerate(raw_segments):

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
            preceding = raw_segments[i - num_bookends: i]
            segment_obj.text_preceding += [x['text'] for x in preceding]
        if i < num_segments - num_bookends:
            following = raw_segments[i + 1: i + num_bookends + 1]
            segment_obj.text_following += [x['text'] for x in following]

        segments.append(segment_obj)
        full_text += segment_obj.text
        char_index = i_end

    return _Transcript(full_text, segments)


def search_transcript(transcript: _Transcript, text: str) -> list[Match]:
    """Search for text in the transcript, returning a list of matches."""
    matches: list[Match] = []
    indexes = get_matched_indexes(transcript.full_text, text.lower())

    for i_start, i_end in indexes:
        matching_segments = []
        for segment in transcript.segments:
            if segment.i_end == i_start:
                i_start += 1
            if segment.i_start <= i_start <= segment.i_end or \
                    segment.i_start <= i_end <= segment.i_end:
                matching_segments.append(segment)

        match = build_match(text, matching_segments)
        matches.append(match)
    return matches
