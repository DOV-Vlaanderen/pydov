"""Module grouping common tests for all search modules."""

import datetime
import numpy as np
import pytest

from pydov.search.bodemlocatie import BodemlocatieSearch
from pydov.search.bodemdiepteinterval import BodemdiepteintervalSearch
from pydov.search.bodemmonster import BodemmonsterSearch
from pydov.search.bodemobservatie import BodemobservatieSearch
from pydov.search.bodemsite import BodemsiteSearch
from pydov.search.bodemclassificatie import BodemclassificatieSearch
from pydov.search.boring import BoringSearch
from pydov.search.generic import WfsSearch
from pydov.search.grondmonster import GrondmonsterSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.search.grondwatermonster import GrondwaterMonsterSearch
from pydov.search.grondwatervergunning import GrondwaterVergunningSearch
from pydov.search.interpretaties import (
    FormeleStratigrafieSearch, GecodeerdeLithologieSearch,
    GeotechnischeCoderingSearch, HydrogeologischeStratigrafieSearch,
    InformeleHydrogeologischeStratigrafieSearch, InformeleStratigrafieSearch,
    LithologischeBeschrijvingenSearch, QuartairStratigrafieSearch)
from pydov.search.sondering import SonderingSearch
from pydov.util.errors import InvalidSearchParameterError
from pydov.util.location import Point, WithinDistance
from tests.abstract import ServiceCheck

from pydov.search.abstract import AbstractCommon

search_objects = [BodemsiteSearch(),
                  BodemlocatieSearch(),
                  BodemdiepteintervalSearch(),
                  BodemobservatieSearch(),
                  BodemmonsterSearch(),
                  BodemclassificatieSearch(),
                  BoringSearch(),
                  SonderingSearch(),
                  GrondwaterFilterSearch(),
                  GrondwaterMonsterSearch(),
                  GrondwaterVergunningSearch(),
                  FormeleStratigrafieSearch(),
                  InformeleHydrogeologischeStratigrafieSearch(),
                  GeotechnischeCoderingSearch(),
                  QuartairStratigrafieSearch(),
                  InformeleStratigrafieSearch(),
                  HydrogeologischeStratigrafieSearch(),
                  GecodeerdeLithologieSearch(),
                  LithologischeBeschrijvingenSearch(),
                  GrondmonsterSearch(),
                  WfsSearch('dov-pub:Opdrachten')]


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
@pytest.mark.skipif(not ServiceCheck.service_ok(),
                    reason="DOV service is unreachable")
@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_location(objectsearch):
    """Test the get_description method.

    Test whether the method returns a non-empty string.

    Parameters
    ----------
    objectsearch : pytest.fixture
        An instance of a subclass of AbstractTestSearch to perform search
        operations on the corresponding DOV type.

    """
    objectsearch.search(location=WithinDistance(Point(100000, 100000), 100))


@pytest.mark.online
@pytest.mark.skipif(not ServiceCheck.service_ok(),
                    reason="DOV service is unreachable")
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
@pytest.mark.skipif(not ServiceCheck.service_ok(),
                    reason="DOV service is unreachable")
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


@pytest.mark.online
@pytest.mark.skipif(not ServiceCheck.service_ok(),
                    reason="DOV service is unreachable")
@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_wfs_no_primary_key(objectsearch):
    """Test the search method with return fields from WFS but not
    including the primary key column.

    Test whether the output dataframe contains the resolved WFS data.
    """
    wfs_return_fields = [
        f['name'] for f in objectsearch.get_fields().values()
        if f['cost'] == 1 and f['type'] == 'float' and f['notnull']
        and 'pkey' not in f['name']]

    if len(wfs_return_fields) > 0:
        field = wfs_return_fields[0]

        df = objectsearch.search(max_features=1, return_fields=(field,))
        assert not np.isnan(df[field][0])


def test_typeconvert_datetime():
    """Test the type conversion function for datetime strings."""

    # Zulu time
    x = AbstractCommon._typeconvert('2023-02-07T09:19:24Z', 'datetime')
    assert isinstance(x, datetime.datetime)
    assert x == datetime.datetime(2023, 2, 7, 10, 19, 24, 0)

    # Brussels time
    x = AbstractCommon._typeconvert('2023-02-07T09:19:24+0100', 'datetime')
    assert isinstance(x, datetime.datetime)
    assert x == datetime.datetime(
        2023, 2, 7, 9, 19, 24, 0,
        datetime.timezone(datetime.timedelta(hours=1)))

    # Brussels time, with colon
    x = AbstractCommon._typeconvert('2023-02-07T09:19:24+01:00', 'datetime')
    assert isinstance(x, datetime.datetime)
    assert x == datetime.datetime(
        2023, 2, 7, 9, 19, 24, 0,
        datetime.timezone(datetime.timedelta(hours=1)))

    # With milliseconds
    x = AbstractCommon._typeconvert('2023-02-07T09:19:24.123+01:00', 'datetime')
    assert isinstance(x, datetime.datetime)
    assert x == datetime.datetime(
        2023, 2, 7, 9, 19, 24, 123,
        datetime.timezone(datetime.timedelta(hours=1)))

    # With more milliseconds
    x = AbstractCommon._typeconvert(
        '2023-02-07T09:19:24.123456+01:00', 'datetime')
    assert isinstance(x, datetime.datetime)
    assert x == datetime.datetime(
        2023, 2, 7, 9, 19, 24, 123456,
        datetime.timezone(datetime.timedelta(hours=1)))
