import math
from dataclasses import dataclass


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
