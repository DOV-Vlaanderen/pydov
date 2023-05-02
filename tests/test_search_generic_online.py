"""Module grouping online tests for the generic search module."""

import pytest

from pydov.search.generic import WfsSearch
from tests.abstract import ServiceCheck


class TestWfsSearchOnline:
    """Class grouping online tests for the generic search module. """

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_multiple_types(self):
        """Test whether multiple instances of WfsSearch don't share their
        fields.
        """
        search1 = WfsSearch('dov-pub:Opdrachten')
        search2 = WfsSearch('erosie:erosie_gemeente')

        assert search1.get_fields() != search2.get_fields()
