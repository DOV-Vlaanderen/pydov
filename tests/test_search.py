"""Module grouping tests for the boring search module."""
import glob

import pytest

import owslib
import pydov
from owslib.etree import etree
from owslib.wfs import WebFeatureService
from pydov.search.boring import BoringSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch

from numpy.compat import unicode

from pydov.search.interpretaties import InformeleStratigrafieSearch
from pydov.search.interpretaties import HydrogeologischeStratigrafieSearch
from pydov.search.interpretaties import GecodeerdeLithologieSearch
from pydov.search.interpretaties import LithologischeBeschrijvingenSearch
from pydov.util.errors import (
    InvalidSearchParameterError,
)


search_objects = [BoringSearch(),
                  GrondwaterFilterSearch(),
                  InformeleStratigrafieSearch(),
                  HydrogeologischeStratigrafieSearch(),
                  GecodeerdeLithologieSearch(),
                  LithologischeBeschrijvingenSearch(),]


@pytest.fixture(scope='module')
def mp_wfs(monkeymodule):
    """Monkeypatch the call to the remote GetCapabilities request.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.

    """
    def read(*args, **kwargs):
        with open('tests/data/util/owsutil/wfscapabilities.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
            data = etree.fromstring(data)
        return data

    monkeymodule.setattr(
        owslib.feature.common.WFSCapabilitiesReader, 'read', read)


@pytest.fixture(scope='module')
def wfs(mp_wfs):
    """PyTest fixture providing an instance of a WebFeatureService based on
    a local copy of a GetCapabilities request.

    Parameters
    ----------
    mp_wfs : pytest.fixture
        Monkeypatch the call to the remote GetCapabilities request.

    Returns
    -------
    owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.

    """
    return WebFeatureService(
        url="https://www.dov.vlaanderen.be/geoserver/wfs",
        version="1.1.0")


@pytest.fixture()
def mp_remote_fc_notfound(monkeypatch):
    """Monkeypatch the call to get an inexistent remote featurecatalogue.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_fc(*args, **kwargs):
        with open('tests/data/util/owsutil/fc_featurecatalogue_notfound.xml',
                  'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.util.owsutil, '__get_remote_fc', __get_remote_fc)


@pytest.fixture(scope='module')
def mp_remote_md(wfs, monkeymodule, request):
    """Monkeypatch the call to get the remote metadata of the layer.

    This monkeypatch requires a module variable ``location_md_metadata``
    with the path to the md_metadata file on disk.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """
    def __get_remote_md(*args, **kwargs):
        file_path = getattr(request.module, "location_md_metadata")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeymodule.setattr(pydov.util.owsutil, '__get_remote_md',
                         __get_remote_md)


@pytest.fixture(scope='module')
def mp_remote_fc(monkeymodule, request):
    """Monkeypatch the call to get the remote feature catalogue.

    This monkeypatch requires a module variable
    ``location_fc_featurecatalogue`` with the path to the fc_featurecatalogue
    file on disk.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """
    def __get_remote_fc(*args, **kwargs):
        file_path = getattr(request.module, "location_fc_featurecatalogue")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeymodule.setattr(pydov.util.owsutil, '__get_remote_fc',
                         __get_remote_fc)


@pytest.fixture(scope='module')
def mp_remote_describefeaturetype(monkeymodule, request):
    """Monkeypatch the call to a remote DescribeFeatureType.

    This monkeypatch requires a module variable
    ``location_wfs_describefeaturetype`` with the path to the
    wfs_describefeaturetype file on disk.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """
    def __get_remote_describefeaturetype(*args, **kwargs):
        file_path = getattr(request.module, "location_wfs_describefeaturetype")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeymodule.setattr(pydov.util.owsutil,
                         '__get_remote_describefeaturetype',
                         __get_remote_describefeaturetype)


@pytest.fixture(scope='module')
def wfs_getfeature(request):
    """PyTest fixture providing a WFS GetFeature response.

    This monkeypatch requires a module variable ``location_wfs_getfeature``
    with the path to the wfs_getfeature file on disk.

    Parameters
    ----------
    request : pytest.fixtue
        PyTest fixture providing request context.

    Returns
    -------
    str
        WFS response of a GetFeature call to the dov-pub:Boringen layer.

    """
    file_path = getattr(request.module, "location_wfs_getfeature")
    with open(file_path, 'r') as f:
        data = f.read()
        return data


@pytest.fixture(scope='module')
def wfs_feature(request):
    """PyTest fixture providing an XML of a WFS feature element.

    This monkeypatch requires a module variable ``location_wfs_feature``
    with the path to the wfs_feature file on disk.

    Parameters
    ----------
    request : pytest.fixtue
        PyTest fixture providing request context.

    Returns
    -------
    etree.Element
        XML element representing a single record of the Boring WFS layer.

    """
    file_path = getattr(request.module, "location_wfs_feature")
    with open(file_path, 'r') as f:
        return etree.fromstring(f.read())


@pytest.fixture(scope='module')
def mp_remote_wfs_feature(monkeymodule, request):
    """Monkeypatch the call to get WFS features.

    This monkeypatch requires a module variable ``location_wfs_getfeature``
    with the path to the wfs_getfeature file on disk.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """
    def __get_remote_wfs_feature(*args, **kwargs):
        file_path = getattr(request.module, "location_wfs_getfeature")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeymodule.setattr(pydov.util.owsutil,
                         'wfs_get_feature',
                         __get_remote_wfs_feature)


@pytest.fixture(scope='module')
def mp_dov_xml(monkeymodule, request):
    """Monkeypatch the call to get the remote XML data.

    This monkeypatch requires a module variable ``location_dov_xml``
    with the path to the dov_xml file on disk.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """

    def _get_xml_data(*args, **kwargs):
        file_path = getattr(request.module, "location_dov_xml")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeymodule.setattr(pydov.types.abstract.AbstractDovType,
                         '_get_xml_data', _get_xml_data)


@pytest.fixture()
def mp_dov_xml_broken(monkeypatch):
    """Monkeypatch the call to break the fetching of remote XML data.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """

    def _get_xml_data(*args, **kwargs):
        raise RuntimeError

    monkeypatch.setattr(pydov.types.abstract.AbstractDovType,
                        '_get_xml_data', _get_xml_data)


@pytest.fixture()
def mp_remote_xsd(monkeymodule, request):
    """Monkeypatch the call to get the remote XSD schemas.

    This monkeypatch requires a module variable ``location_xsd_base``
    with a glob expression to the XSD file(s) on disk.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.
    request : pytest.fixtue
        PyTest fixture providing request context.

    """

    def _get_remote_xsd(*args, **kwargs):
        xsd_base_path = getattr(request.module, "location_xsd_base")
        schemas = []

        for xsd_file in glob.glob(xsd_base_path):
            with open(xsd_file, 'r') as f:
                data = f.read()
                if type(data) is not bytes:
                    data = data.encode('utf-8')
                schemas.append(etree.fromstring(data))

        return schemas

    monkeymodule.setattr(pydov.search.abstract.AbstractSearch,
                         '_get_remote_xsd_schemas', _get_remote_xsd)


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
