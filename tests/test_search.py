"""Module grouping tests for the boring search module."""

import pytest

from pydov.search.boring import BoringSearch
from pydov.search.grondmonster import GrondmonsterSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.search.grondwatermonster import GrondwaterMonsterSearch
from pydov.search.interpretaties import (
    FormeleStratigrafieSearch, GecodeerdeLithologieSearch,
    GeotechnischeCoderingSearch, HydrogeologischeStratigrafieSearch,
    InformeleHydrogeologischeStratigrafieSearch, InformeleStratigrafieSearch,
    LithologischeBeschrijvingenSearch, QuartairStratigrafieSearch)
from pydov.search.sondering import SonderingSearch
from pydov.util.errors import InvalidSearchParameterError
from pydov.util.location import Point, WithinDistance
from tests.abstract import service_ok

search_objects = [BoringSearch(),
                  SonderingSearch(),
                  GrondwaterFilterSearch(),
                  GrondwaterMonsterSearch(),
                  FormeleStratigrafieSearch(),
                  InformeleHydrogeologischeStratigrafieSearch(),
                  GeotechnischeCoderingSearch(),
                  QuartairStratigrafieSearch(),
                  InformeleStratigrafieSearch(),
                  HydrogeologischeStratigrafieSearch(),
                  GecodeerdeLithologieSearch(),
                  LithologischeBeschrijvingenSearch(),
                  GrondmonsterSearch()]


@pytest.mark.parametrize("objectsearch", search_objects)
def test_get_description(mp_wfs, objectsearch):
    """Test the get_description method.

    Test whether the method returns a non-empty string.

    Parameters
    ----------
    mp_wfs : pytest.fixture
        Monkeypatch the call to the remote GetCapabilities request.
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    description = objectsearch.get_description()

    assert isinstance(description, str)
    assert len(description) > 0


@pytest.mark.online
@pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_location(objectsearch):
    """Test the get_description method.

    Test whether the method returns a non-empty string.

    Parameters
    ----------
    mp_wfs : pytest.fixture
        Monkeypatch the call to the remote GetCapabilities request.
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    objectsearch.search(location=WithinDistance(Point(100000, 100000), 100))


@pytest.mark.online
@pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_maxfeatures(objectsearch):
    """Test the search method with a max_features parameter.

    Test whether no error is raised.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    objectsearch.search(location=WithinDistance(Point(100000, 100000), 100),
                        max_features=10)


@pytest.mark.online
@pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_maxfeatures_only(objectsearch):
    """Test the search method with only the max_features parameter.

    Test whether no error is raised.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    objectsearch.search(max_features=1)


@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_nolocation_noquery(objectsearch):
    """Test the search method without providing a location or a query.

    Test whether an InvalidSearchParameterError is raised.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    with pytest.raises(InvalidSearchParameterError):
        objectsearch.search(location=None, query=None)


@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_both_location_query_wrongquerytype(objectsearch):
    """Test the search method providing both a location and a query,
    using a query with an invalid type.

    Test whether an InvalidSearchParameterError is raised.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    with pytest.raises(InvalidSearchParameterError):
        objectsearch.search(location=(1, 2, 3, 4),
                            query='computer says no')


@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_query_wrongtype(objectsearch):
    """Test the search method with the query parameter using a wrong
    query type.

    Test whether an InvalidSearchParameterError is raised.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    with pytest.raises(InvalidSearchParameterError):
        objectsearch.search(query='computer says no')
