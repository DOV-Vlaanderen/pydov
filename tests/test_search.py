"""Module grouping tests for the search module."""

import pytest
from owslib.fes import PropertyIsEqualTo

from pydov.util.errors import InvalidSearchParameterError


@pytest.fixture
def boringsearch():
    from pydov.search import BoringSearch
    return BoringSearch()


class TestBoringSearch(object):
    def test_search_nolocation_noquery(self, boringsearch):
        with pytest.raises(InvalidSearchParameterError):
            boringsearch.search(location=None, query=None)

    def test_search_both_location_query(self, boringsearch):
        with pytest.raises(InvalidSearchParameterError):
            query = PropertyIsEqualTo(propertyname='gemeente',
                                      literal='Blankenberge')
            boringsearch.search(location=(1, 2, 3, 4),
                                query=query)
