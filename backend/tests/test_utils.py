import service.utils as utils


def test_get_matched_indexes():
    text = 'hello world'
    search_text = 'world'
    result = utils.get_matched_indexes(text, search_text)
    assert result == [(6, 11)]


def test_get_matched_indexes_multiple():
    text = 'hello world hello world'
    search_text = 'world'
    result = utils.get_matched_indexes(text, search_text)
    assert result == [(6, 11), (18, 23)]


def test_get_matched_indexes_multiple_words():
    text = 'hello world hello world'
    search_text = 'hello world'
    result = utils.get_matched_indexes(text, search_text)
    assert result == [(0, 11), (12, 23)]
