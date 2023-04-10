

from dataclasses import dataclass
from service.text_segment import TextSegment
from service.utils import format_time, get_matched_indexes


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
    full_text = f'{preceding_text} {main_text_lower} {following_text}'
    full_text_original = f'{preceding_text} {main_text_original} {following_text}'

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
