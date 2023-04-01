import re


def get_matched_indexes(text, search_text) -> list[tuple[int, int]]:
    """Return a list of start and end indexes where the search text is found in the text"""
    return [(m.start(), m.end()) for m in re.finditer(search_text, text)]
