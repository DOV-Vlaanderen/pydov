"""Module grouping tests for the pydov.util.owsutil module."""
import copy
import os

import pytest

from pydov.util import dovutil

env_var = "PYDOV_BASE_URL"


@pytest.fixture
def pydov_base_url_environment():
    """Fixture for setting an environment variable with a different base_url.
    """
    old_environ = copy.deepcopy(os.environ)
    os.environ[env_var] = 'https://dov/'

    yield

    os.environ = old_environ


class TestDovutil(object):
    """Class grouping tests for the pydov.util.dovutil module."""

    def test_get_default_dov_base_url_slash(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('/geonetwork') == \
                   'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_default_dov_base_url_multislash(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('/geonetwork/srv') == \
                   'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_default_dov_base_url_endslash(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('/geonetwork/') == \
                   'https://www.dov.vlaanderen.be/geonetwork/'

    def test_get_default_dov_base_url_noslash(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('geonetwork') == \
                   'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_default_dov_base_url_noslash_multi(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('geonetwork/srv') == \
                   'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_default_dov_base_url_noslash_end(self):
        if env_var not in os.environ:
            assert dovutil.build_dov_url('geonetwork/') == \
                   'https://www.dov.vlaanderen.be/geonetwork/'

    def test_get_dov_base_url_slash(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('/geonetwork') == \
            'https://dov/geonetwork'

    def test_get_dov_base_url_multislash(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('/geonetwork/srv') == \
            'https://dov/geonetwork/srv'

    def test_get_dov_base_url_endslash(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('/geonetwork/') == \
            'https://dov/geonetwork/'

    def test_get_dov_base_url_noslash(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('geonetwork') == \
            'https://dov/geonetwork'

    def test_get_dov_base_url_noslash_multi(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('geonetwork/srv') == \
            'https://dov/geonetwork/srv'

    def test_get_dov_base_url_noslash_end(self, pydov_base_url_environment):
        assert env_var in os.environ
        assert dovutil.build_dov_url('geonetwork/') == \
            'https://dov/geonetwork/'
