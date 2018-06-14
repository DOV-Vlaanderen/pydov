# -*- encoding: utf-8 -*-

import pytest

from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch
from tests.abstract import (
    AbstractTestSearch,
    service_ok,
)


class TestEncoding(AbstractTestSearch):
    """Class grouping tests related to encoding issues."""

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_search(self):
        """Test the search method with strange character in the output.

        Test whether the output has the correct encoding.

        """
        boringsearch = BoringSearch()
        query = PropertyIsEqualTo(
            propertyname='pkey_boring',
            literal='https://www.dov.vlaanderen.be/data/boring/1928-031159')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'uitvoerder'))

        assert df.uitvoerder[0] == 'Societé Belge des Bétons'
