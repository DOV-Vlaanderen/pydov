"""Module grouping tests for the search module."""

import pytest


@pytest.fixture
def boringsearch():
    from pydov.search import BoringSearch
    return BoringSearch()


class TestBoringSearch(object):
    def test_description(self, boringsearch):
        assert type(boringsearch.get_description()) is str
        assert len(boringsearch.get_description()) > 0
