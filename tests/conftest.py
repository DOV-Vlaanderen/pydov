"""Module grouping session scoped PyTest fixtures."""

import datetime
import glob
import os
import tempfile

import owslib
import pytest
from _pytest.monkeypatch import MonkeyPatch
from owslib.etree import etree
from owslib.feature.schema import _construct_schema, _get_elements
from owslib.iso import MD_Metadata
from owslib.util import findall
from owslib.wfs import WebFeatureService

import pydov
from pydov import Hooks
from pydov.util import owsutil
from pydov.util.caching import GzipTextFileCache, PlainTextFileCache
from pydov.util.dovutil import build_dov_url


def pytest_runtest_setup():
    pydov.hooks = Hooks()


def pytest_configure(config):
    config.addinivalue_line("markers",
                            "online: mark test that requires internet access")


@pytest.fixture(scope='module')
def monkeymodule():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope='module')
def mp_wfs(monkeymodule):
    """Monkeypatch the call to the remote GetCapabilities request.

    Parameters
    ----------
    monkeymodule : pytest.fixture
        PyTest monkeypatch fixture with module scope.

    """
    def read(*args, **kwargs):
        with open('tests/data/util/owsutil/wfscapabilities.xml', 'r',
                  encoding='utf-8') as f:
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
        url=build_dov_url('geoserver/wfs'), version="1.1.0")


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
        return MD_Metadata(etree.fromstring(data).find(
            './{http://www.isotc211.org/2005/gmd}MD_Metadata'))

    monkeymodule.setattr(pydov.util.owsutil, 'get_remote_metadata',
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
def mp_get_schema(monkeymodule, request):
    def __get_schema(*args, **kwargs):
        file_path = getattr(request.module, "location_wfs_describefeaturetype")
        with open(file_path, 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')

        root = etree.fromstring(data)

        typename = root.find(
            './{http://www.w3.org/2001/XMLSchema}element').get('name')

        if ":" in typename:
            typename = typename.split(":")[1]
        type_element = findall(
            root,
            "{http://www.w3.org/2001/XMLSchema}element",
            attribute_name="name",
            attribute_value=typename,
        )[0]
        complex_type = type_element.attrib["type"].split(":")[1]
        elements = _get_elements(complex_type, root)
        nsmap = None
        if hasattr(root, "nsmap"):
            nsmap = root.nsmap
        return _construct_schema(elements, nsmap)

    monkeymodule.setattr(pydov.search.abstract.AbstractSearch, '_get_schema',
                         __get_schema)


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
        with open(file_path, 'r', encoding="utf-8") as f:
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
            with open(xsd_file, 'r', encoding="utf-8") as f:
                data = f.read()
                if type(data) is not bytes:
                    data = data.encode('utf-8')
                schemas.append(etree.fromstring(data))

        return schemas

    monkeymodule.setattr(pydov.search.abstract.AbstractSearch,
                         '_get_remote_xsd_schemas', _get_remote_xsd)


@pytest.fixture
def md_metadata(wfs, mp_remote_md):
    """PyTest fixture providing a MD_Metadata instance of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    mp_remote_md : pytest.fixture
        Monkeypatch the call to get the remote metadata of the
        dov-pub:Boringen layer.

    Returns
    -------
    owslib.iso.MD_Metadata
        Parsed metadata describing the Boringen WFS layer in more detail,
        in the ISO 19115/19139 format.

    """
    contentmetadata = wfs.contents['dov-pub:Boringen']
    return owsutil.get_remote_metadata(contentmetadata)


@pytest.fixture
def mp_remote_xml(monkeypatch):
    """Monkeypatch the call to get the remote Boring XML data.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """

    def _get_remote_data(*args, **kwargs):
        with open('tests/data/types/boring/boring.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.util.caching.AbstractFileCache,
                        '_get_remote', _get_remote_data)


@pytest.fixture
def plaintext_cache(request):
    """Fixture for a temporary cache.

    This fixture should be parametrized, with a list of parameters in the
    order described below.

    Parameters
    ----------
    max_age : datetime.timedelta
        The maximum age to use for the cache.

    """
    orig_cache = pydov.cache

    if len(request.param) == 0:
        max_age = datetime.timedelta(seconds=1)
    else:
        max_age = request.param[0]

    plaintext_cache = PlainTextFileCache(
        cachedir=os.path.join(tempfile.gettempdir(), 'pydov_tests'),
        max_age=max_age)
    pydov.cache = plaintext_cache

    yield plaintext_cache

    plaintext_cache.remove()
    pydov.cache = orig_cache


@pytest.fixture
def gziptext_cache(request):
    """Fixture for a temporary cache.

    This fixture should be parametrized, with a list of parameters in the
    order described below.

    Parameters
    ----------
    max_age : datetime.timedelta
        The maximum age to use for the cache.

    """
    orig_cache = pydov.cache

    if len(request.param) == 0:
        max_age = datetime.timedelta(seconds=1)
    else:
        max_age = request.param[0]

    gziptext_cache = GzipTextFileCache(
        cachedir=os.path.join(tempfile.gettempdir(), 'pydov_tests'),
        max_age=max_age)
    pydov.cache = gziptext_cache

    yield gziptext_cache

    gziptext_cache.remove()
    pydov.cache = orig_cache


@pytest.fixture
def nocache():
    """Fixture to temporarily disable caching."""
    orig_cache = pydov.cache
    pydov.cache = None
    yield
    pydov.cache = orig_cache
