
import json
from service.transcript import build_transcript, search_transcript


def open_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


test_data = open_json('./mocks/speedlore.json')['segments']


def test_search():
    t = build_transcript(test_data)
    matches = search_transcript(t, 'goldeneye')
    assert len(matches) == 11


def test_search_across_segments():
    t = build_transcript(test_data)
    matches = search_transcript(t, 'even as the years')
    assert len(matches) == 1


def test_matches():
    t = build_transcript(test_data)
    matches = search_transcript(t, 'even as the years')
    match = matches[0]
    print(match)
    assert match.exact_text == 'even as the years'
    assert match.preceding_text == 'always cool to see him come back up here on these uh deal Decay episodes'
    assert match.following_text == 'go by you know so nice job Lou'
