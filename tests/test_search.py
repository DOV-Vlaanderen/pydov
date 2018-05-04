"""Module grouping tests for the boring search module."""

import datetime
import sys

import pytest

from pydov.search.boring import BoringSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch

from numpy.compat import unicode

from tests.test_util_owsutil import (
    mp_wfs,
    mp_remote_describefeaturetype,
    mp_remote_md,
    mp_remote_fc,
    wfs,
)
from pydov.util.errors import (
    InvalidSearchParameterError
)


search_objects = [BoringSearch(),
                  GrondwaterFilterSearch()]

@pytest.mark.parametrize("objectsearch", search_objects)
def test_get_description(mp_wfs, objectsearch):
    """Test the get_description method.

    Test whether the method returns a non-empty string.

    Parameters
    ----------
    mp_wfs : pytest.fixture
        Monkeypatch the call to the remote GetCapabilities request.
    boringsearch : pytest.fixture returning pydov.search.BoringSearch
        An instance of BoringSearch to perform search operations on the DOV
        type 'Boring'.

    """
    description = objectsearch.get_description()

    assert type(description) in (str, unicode)
    assert len(description) > 0

# to adapt, as the mp_* are still boring specific
@pytest.mark.parametrize("objectsearch", search_objects)
def test_get_fields(mp_wfs, mp_remote_describefeaturetype,
                    mp_remote_md, mp_remote_fc, objectsearch):
    """Test the get_fields method.

    Test whether the returned fields match the format specified in the
    documentation.

    Parameters
    ----------
    mp_wfs : pytest.fixture
        Monkeypatch the call to the remote GetCapabilities request.
    mp_remote_describefeaturetype : pytest.fixture
        Monkeypatch the call to a remote DescribeFeatureType of the
        dov-pub:Boringen layer.
    mp_remote_md : pytest.fixture
        Monkeypatch the call to get the remote metadata of the
        dov-pub:Boringen layer.
    mp_remote_fc : pytest.fixture
        Monkeypatch the call to get the remote feature catalogue of the
        dov-pub:Boringen layer.
    boringsearch : pytest.fixture returning pydov.search.BoringSearch
        An instance of BoringSearch to perform search operations on the DOV
        type 'Boring'.

    """
    fields = objectsearch.get_fields()

    assert type(fields) is dict

    for field in fields:
        assert type(field) in (str, unicode)

        f = fields[field]
        assert type(f) is dict

        assert 'name' in f
        assert type(f['name']) in (str, unicode)
        assert f['name'] == field

        assert 'definition' in f
        assert type(f['name']) in (str, unicode)

        assert 'type' in f
        assert type(f['type']) in (str, unicode)
        assert f['type'] in ['string', 'float', 'integer', 'date',
                             'boolean']

        assert 'notnull' in f
        assert type(f['notnull']) is bool

        assert 'cost' in f
        assert type(f['cost']) is int
        assert f['cost'] > 0

        if 'values' in f:
            assert sorted(f.keys()) == [
                'cost', 'definition', 'name', 'notnull', 'type', 'values']
            for v in f['values']:
                if f['type'] == 'string':
                    assert type(v) in (str, unicode)
                elif f['type'] == 'float':
                    assert type(v) is float
                elif f['type'] == 'integer':
                    assert type(v) is int
                elif f['type'] == 'date':
                    assert type(v) is datetime.date
                elif f['type'] == 'boolean':
                    assert type(v) is bool
        else:
            assert sorted(f.keys()) == ['cost', 'definition', 'name',
                                        'notnull', 'type']

@pytest.mark.parametrize("objectsearch", search_objects)
def test_search_nolocation_noquery(objectsearch):
    """Test the search method without providing a location or a query.

    Test whether an InvalidSearchParameterError is raised.

    Parameters
    ----------
    boringsearch : pytest.fixture returning pydov.search.BoringSearch
        An instance of BoringSearch to perform search operations on the DOV
        type 'Boring'.

    """
    with pytest.raises(InvalidSearchParameterError):
        objectsearch.search(location=None, query=None)
