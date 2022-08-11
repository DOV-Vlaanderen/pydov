import copy
import datetime

import pytest
from owslib.etree import etree
from owslib.fes2 import PropertyIsEqualTo

import pydov
from pydov.search.boring import BoringSearch
from pydov.util.hooks import (AbstractInjectHook, AbstractReadHook, Hooks,
                              SimpleStatusHook)
from pydov.util.location import AbstractLocationFilter
from tests.abstract import ServiceCheck


@pytest.fixture
def test_hook_count():
    """PyTest fixture temporarily disabling default hooks and installing
    HookCounter."""
    orig_hooks = pydov.hooks

    pydov.hooks = Hooks(
        (HookCounter(),)
    )
    yield

    pydov.hooks = orig_hooks


@pytest.fixture
def test_hook_types():
    """PyTest fixture temporarily disabling default hooks and installing
    HookTester."""
    orig_hooks = pydov.hooks

    pydov.hooks = Hooks(
        (HookTypeTester(),)
    )
    yield

    pydov.hooks = orig_hooks


@pytest.fixture
def test_hook_inject():
    """PyTest fixture temporarily disabling default hooks and installing
    HookInjecter."""
    orig_hooks = pydov.hooks

    pydov.hooks = Hooks(
        (HookInjecter(),)
    )
    yield

    pydov.hooks = orig_hooks


class HookCounter(AbstractReadHook, AbstractInjectHook):
    """Hook implementation for testing purposes, counting all event calls."""

    def __init__(self):
        self.count_meta_received = 0
        self.count_inject_meta_response = 0
        self.count_wfs_search_init = 0
        self.count_wfs_search_result = 0
        self.count_wfs_search_result_received = 0
        self.count_inject_wfs_getfeature_response = 0
        self.count_xml_received = 0
        self.count_inject_xml_response = 0
        self.count_xml_cache_hit = 0
        self.count_xml_stale_hit = 0
        self.count_xml_fetch_error = 0
        self.count_xml_downloaded = 0

    def meta_received(self, url, response):
        self.count_meta_received += 1

    def inject_meta_response(self, url):
        self.count_inject_meta_response += 1

    def wfs_search_init(self, params):
        self.count_wfs_search_init += 1

    def wfs_search_result(self, number_matched, number_returned):
        self.count_wfs_search_result += 1

    def wfs_search_result_received(self, query, features):
        self.count_wfs_search_result_received += 1

    def inject_wfs_getfeature_response(self, query):
        self.count_inject_wfs_getfeature_response += 1

    def xml_received(self, pkey_object, xml):
        self.count_xml_received += 1

    def inject_xml_response(self, pkey_object):
        self.count_inject_xml_response += 1

    def xml_cache_hit(self, pkey_object):
        self.count_xml_cache_hit += 1

    def xml_stale_hit(self, pkey_object):
        self.count_xml_stale_hit += 1

    def xml_downloaded(self, pkey_object):
        self.count_xml_downloaded += 1

    def xml_fetch_error(self, pkey_object):
        self.count_xml_fetch_error += 1


class HookTypeTester(AbstractReadHook, AbstractInjectHook):
    """Hook implementation for testing purposes, testing arguments of all
    event calls."""

    def meta_received(self, url, response):
        assert url is not None
        assert response is not None
        assert isinstance(url, str)
        assert isinstance(response, bytes)

    def inject_meta_response(self, url):
        assert url is not None
        assert isinstance(url, str)

    def wfs_search_init(self, params):
        assert params is not None
        assert isinstance(params, dict)

        assert 'typename' in params
        assert isinstance(params['typename'], str)

        assert 'location' in params
        assert params['location'] is None or \
            isinstance(params['location'], str)

        assert 'sort_by' in params
        assert params['sort_by'] is None or \
            isinstance(params['sort_by'], str)

        assert 'max_features' in params
        assert params['max_features'] is None or \
            isinstance(params['max_features'], int)

        assert 'propertynames' in params
        assert isinstance(params['propertynames'], list)
        for propertyname in params['propertynames']:
            assert isinstance(propertyname, str)

        assert 'geometry_column' in params
        assert isinstance(params['geometry_column'], str)

    def wfs_search_result(self, number_matched, number_returned):
        assert number_matched is not None
        assert isinstance(number_matched, int)
        assert number_matched > 0

        assert number_returned is not None
        assert isinstance(number_returned, int)
        assert number_returned > 0
        assert number_matched >= number_returned

    def wfs_search_result_received(self, query, features):
        assert query is not None
        assert features is not None

    def inject_wfs_getfeature_response(self, query):
        assert query is not None

    def xml_received(self, pkey_object, xml):
        assert pkey_object is not None
        assert xml is not None
        assert isinstance(pkey_object, str)
        assert isinstance(xml, bytes)

    def inject_xml_response(self, pkey_object):
        assert pkey_object is not None
        assert isinstance(pkey_object, str)

    def xml_cache_hit(self, pkey_object):
        assert pkey_object is not None
        assert isinstance(pkey_object, str)

    def xml_stale_hit(self, pkey_object):
        assert pkey_object is not None
        assert isinstance(pkey_object, str)

    def xml_downloaded(self, pkey_object):
        assert pkey_object is not None
        assert isinstance(pkey_object, str)

    def xml_fetch_error(self, pkey_object):
        assert pkey_object is not None
        assert isinstance(pkey_object, str)


class HookInjecter(AbstractReadHook, AbstractInjectHook):
    """Hook implementation for testing purposes, testing response injection."""

    def __init__(self):
        self.wfs_features = None
        self.dov_xml = None

    def wfs_search_result_received(self, query, features):
        """Save the WFS GetFeature response in order to adjust and inject
        later."""
        self.wfs_features = features

    def inject_wfs_getfeature_response(self, query):
        """Adapt the previously saved WFS GetFeature response and inject the
        adapted version."""
        if self.wfs_features is not None:
            tree = copy.deepcopy(self.wfs_features)
            gemeentes = tree.findall(
                './/{http://dov.vlaanderen.be/ocdov/dov-pub}Boringen/'
                '{http://dov.vlaanderen.be/ocdov/dov-pub}gemeente')
            if len(gemeentes) == 0:
                gemeente = etree.Element(
                    '{http://dov.vlaanderen.be/ocdov/dov-pub}gemeente')
                gemeente.text = 'Bevergem'
                boring = tree.find(
                    './/{http://dov.vlaanderen.be/ocdov/dov-pub}Boringen')
                boring.append(gemeente)
            else:
                for g in gemeentes:
                    g.text = 'Bevergem'
            return etree.tostring(tree, encoding='utf-8')

    def xml_received(self, pkey_object, xml):
        """Save the DOV Xml response in order to adjust and inject later."""
        self.dov_xml = xml

    def inject_xml_response(self, pkey_object):
        """Adapt the previously saved DOV XML response and inject the adapted
        version."""
        if self.dov_xml is not None:
            tree = etree.fromstring(self.dov_xml)
            boormethoden = tree.findall(
                './/boring/details/boormethode/methode')
            for b in boormethoden:
                b.text = 'De Pypere 106 T'
            return etree.tostring(tree, encoding='utf-8')


class TestHookCount(object):
    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_wfs_only(self, test_hook_count):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        test_hook_count : pytest.fixture
            Fixture removing default hooks and installing HookCounter.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        boringsearch.search(
            query=query, return_fields=('pkey_boring', 'x', 'y'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_wfs_search_result_received == 1
        assert pydov.hooks[0].count_inject_wfs_getfeature_response == 1

        assert pydov.hooks[0].count_xml_received == 0
        assert pydov.hooks[0].count_inject_xml_response == 0
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 0
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_wfs_and_xml_nocache(self, test_hook_count, nocache):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        test_hook_count : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        nocache : pytest.fixture
            Fixture temporarily disabling caching.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_wfs_search_result_received == 1
        assert pydov.hooks[0].count_inject_wfs_getfeature_response == 1

        assert pydov.hooks[0].count_xml_received == 1
        assert pydov.hooks[0].count_inject_xml_response == 1
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 1
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0

        boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 2
        assert pydov.hooks[0].count_wfs_search_result == 2
        assert pydov.hooks[0].count_wfs_search_result_received == 2
        assert pydov.hooks[0].count_inject_wfs_getfeature_response == 2

        assert pydov.hooks[0].count_xml_received == 2
        assert pydov.hooks[0].count_inject_xml_response == 2
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 2
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    @pytest.mark.parametrize('plaintext_cache',
                             [[datetime.timedelta(minutes=15)]],
                             indirect=['plaintext_cache'])
    def test_wfs_and_xml_cache(self, test_hook_count, plaintext_cache):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        test_hook_count : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        plaintext_cache : pytest.fixture
            Fixture temporarily setting up a testcache with max_age of 1
            second.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_wfs_search_result_received == 1
        assert pydov.hooks[0].count_inject_wfs_getfeature_response == 1

        assert pydov.hooks[0].count_xml_received == 1
        assert pydov.hooks[0].count_inject_xml_response == 2
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 1
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0

        boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 2
        assert pydov.hooks[0].count_wfs_search_result == 2
        assert pydov.hooks[0].count_wfs_search_result_received == 2
        assert pydov.hooks[0].count_inject_wfs_getfeature_response == 2

        assert pydov.hooks[0].count_xml_received == 2
        assert pydov.hooks[0].count_inject_xml_response == 3
        assert pydov.hooks[0].count_xml_cache_hit == 1
        assert pydov.hooks[0].count_xml_downloaded == 1
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0


class TestHookTypes(object):
    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_default_hooks(self, nocache):
        """Test the default hooks by performing a simple search.

        Test whether no exceptions are raised.

        Parameters
        ----------
        nocache : pytest.fixture
            Fixture temporarily disabling caching.

        """
        pydov.hooks = Hooks(
            (SimpleStatusHook(),)
        )

        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        boringsearch.search(query=query)

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_hooks(self, test_hook_types):
        """Test the argument types of the hook events.

        Parameters
        ----------
        test_hook_types : pytest.fixture
            Fixture removing default hooks and installing HookTester.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        boringsearch.search(query=query)


class TestHookInject(object):
    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_hooks_inject(self, test_hook_inject):
        """Test the of the hook inject events.

        Test whether the requests are intercepted correctly.

        Parameters
        ----------
        test_hook_types : pytest.fixture
            Fixture removing default hooks and installing HookTester.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()

        boringsearch.search(query=query)
        df = boringsearch.search(query=query)

        assert df.iloc[0].gemeente == 'Bevergem'
        assert df.iloc[0].boormethode == 'De Pypere 106 T'
