"""Module grouping tests for the pydov.util.owsutil module."""
from pydov.util import dovutil


class TestDovutil(object):
    """Class grouping tests for the pydov.util.dovutil module."""

    def test_get_dov_base_url_slash(self):
        assert dovutil.build_dov_url('/geonetwork') == \
               'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_dov_base_url_multislash(self):
        assert dovutil.build_dov_url('/geonetwork/srv') == \
               'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_dov_base_url_endslash(self):
        assert dovutil.build_dov_url('/geonetwork/') == \
               'https://www.dov.vlaanderen.be/geonetwork/'

    def test_get_dov_base_url_noslash(self):
        assert dovutil.build_dov_url('geonetwork') == \
               'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_dov_base_url_noslash_multi(self):
        assert dovutil.build_dov_url('geonetwork/srv') == \
               'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_dov_base_url_noslash_end(self):
        assert dovutil.build_dov_url('geonetwork/') == \
               'https://www.dov.vlaanderen.be/geonetwork/'
