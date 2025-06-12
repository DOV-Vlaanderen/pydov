"""Module grouping tests for the pydov.util.owsutil module."""
import copy
import os

import pytest

from pydov.util import dovutil

env_var = "PYDOV_BASE_URL"


@pytest.fixture(scope='function')
def pydov_base_url_environment():
    """Fixture for setting an environment variable with a different base_url.
    """
    old_environ = copy.deepcopy(os.environ)
    os.environ[env_var] = 'https://dov/'

    yield

    os.environ = old_environ


@pytest.fixture(scope='function')
def pydov_no_base_url():
    """Fixture for removing the environment variable for a different base_url.
    """
    old_environ = copy.deepcopy(os.environ)
    if env_var in os.environ:
        del (os.environ[env_var])

    yield

    os.environ = old_environ


class TestDovutil(object):
    """Class grouping tests for the pydov.util.dovutil module."""

    def test_get_default_dov_base_url_slash(self, pydov_no_base_url):
        assert dovutil.build_dov_url('/geonetwork') == \
            'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_default_dov_base_url_multislash(self, pydov_no_base_url):
        assert dovutil.build_dov_url('/geonetwork/srv') == \
            'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_default_dov_base_url_endslash(self, pydov_no_base_url):
        assert dovutil.build_dov_url('/geonetwork/') == \
            'https://www.dov.vlaanderen.be/geonetwork/'

    def test_get_default_dov_base_url_noslash(self, pydov_no_base_url):
        assert dovutil.build_dov_url('geonetwork') == \
            'https://www.dov.vlaanderen.be/geonetwork'

    def test_get_default_dov_base_url_noslash_multi(self, pydov_no_base_url):
        assert dovutil.build_dov_url('geonetwork/srv') == \
            'https://www.dov.vlaanderen.be/geonetwork/srv'

    def test_get_default_dov_base_url_noslash_end(self, pydov_no_base_url):
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

    def test_build_dov_sparql_request(self, pydov_no_base_url):
        assert env_var not in os.environ

        request = dovutil.build_dov_sparql_request(
            'select ?s where {?s ?p ?o} limit 1')

        assert request.url == \
            'https://data.bodemenondergrond.vlaanderen.be/sparql'

        assert request.headers['Accept'] == 'application/rdf+xml'

    def test_build_dov_sparql_request_oefen(self):
        os.environ[env_var] = 'https://oefen.dov.vlaanderen.be/'

        request = dovutil.build_dov_sparql_request(
            'select ?s where {?s ?p ?o} limit 1')

        assert request.url == \
            'https://data-oefen.bodemenondergrond.vlaanderen.be/sparql'
