
import json
from service.transcript import Transcript


def open_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


test_data = open_json('./mocks/speedlore.json')['segments']


def mock_fetch_raw_transcript(self):
    self._raw_transcript = test_data


Transcript._fetch_transcript = mock_fetch_raw_transcript


def test_search():
    t = Transcript('video_id')
    t.process()
    matches = t.search('goldeneye')
    assert len(matches) == 11


def test_search_across_segments():
    t = Transcript('video_id')
    t.process()
    matches = t.search('even as the years')
    assert len(matches) == 1


def test_matches():
    t = Transcript('video_id')
    t.process()
    matches = t.search('even as the years')
    match = matches[0]
    print(match)
    assert match.exact_text == 'even as the years'
    assert match.preceding_text == 'always cool to see him come back up here on these uh deal Decay episodes'
    assert match.following_text == 'go by you know so nice job Lou'
