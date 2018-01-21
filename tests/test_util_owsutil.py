"""Module grouping tests for the pydov.util.owsutil module."""

import sys

import owslib
import pytest
from numpy.compat import unicode
from owslib.etree import etree
from owslib.iso import MD_Metadata
from owslib.util import nspath_eval
from owslib.wfs import WebFeatureService

from pydov.util import owsutil
from pydov.util.errors import (
    MetadataNotFoundError,
    FeatureCatalogueNotFoundError,
)


@pytest.fixture
def mp_wfs(monkeypatch):
    """Monkeypatch the call to the remote GetCapabilities request.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def read(*args, **kwargs):
        with open('tests/data/util/owsutil/wfscapabilities.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
            data = etree.fromstring(data)
        return data

    monkeypatch.setattr(
        owslib.feature.common.WFSCapabilitiesReader, 'read', read)


@pytest.fixture
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


@pytest.fixture
def mp_remote_md(wfs, monkeypatch):
    """Monkeypatch the call to get the remote metadata of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_md(*args, **kwargs):
        with open('tests/data/util/owsutil/md_metadata.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_md.func_code',
                            __get_remote_md.func_code)
    else:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_md.__code__',
                            __get_remote_md.__code__)


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
def mp_remote_fc(monkeypatch):
    """Monkeypatch the call to get the remote feature catalogue of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_fc(*args, **kwargs):
        with open('tests/data/util/owsutil/fc_featurecatalogue.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.func_code',
                            __get_remote_fc.func_code)
    else:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.__code__',
                            __get_remote_fc.__code__)


@pytest.fixture
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

    if sys.version_info[0] < 3:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.func_code',
                            __get_remote_fc.func_code)
    else:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.__code__',
                            __get_remote_fc.__code__)


@pytest.fixture
def mp_remote_describefeaturetype(monkeypatch):
    """Monkeypatch the call to a remote DescribeFeatureType of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_describefeaturetype(*args, **kwargs):
        with open('tests/data/util/owsutil/wfsdescribefeaturetype.xml',
                  'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr(
            'pydov.util.owsutil.__get_remote_describefeaturetype.func_code',
            __get_remote_describefeaturetype.func_code)
    else:
        monkeypatch.setattr(
            'pydov.util.owsutil.__get_remote_describefeaturetype.__code__',
            __get_remote_describefeaturetype.__code__)


class TestOwsutil(object):
    """Class grouping tests for the pydov.util.owsutil module."""

    def test_get_csw_base_url(self, wfs):
        """Test the owsutil.get_csw_base_url method.

        Test whether the CSW base URL of the dov-pub:Boringen layer is correct.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contentmetadata = wfs.contents['dov-pub:Boringen']
        assert owsutil.get_csw_base_url(contentmetadata) == \
               'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw'

    def test_get_csw_base_url_nometadataurls(self, wfs):
        """Test the owsutil.get_csw_base_url method for a layer without
        metdata urls.

        Test whether a MetadataNotFoundError is raised.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contentmetadata = wfs.contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_csw_base_url(contentmetadata)

    def test_get_featurecatalogue_uuid(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method.

        Test whether the featurecatalogue uuid of the dov-pub:Boringen layer
        is correct.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        assert owsutil.get_featurecatalogue_uuid(md_metadata) == \
               'c0cbd397-520f-4ee1-aca7-d70e271eeed6'

    def test_get_featurecatalogue_uuid_nocontentinfo(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method when the
        metadata is missing the gmd:contentInfo element.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        root = tree.find('{http://www.isotc211.org/2005/gmd}MD_Metadata')
        for ci in tree.findall(
                './/{http://www.isotc211.org/2005/gmd}contentInfo'):
            root.remove(ci)
        md_metadata.xml = etree.tostring(tree)

        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_featurecatalogue_uuid_nouuidref(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method when the
        gmd:contentInfo element is missing a 'uuidref' attribute.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        for ci in tree.findall(nspath_eval(
            'gmd:MD_Metadata/gmd:contentInfo/'
            'gmd:MD_FeatureCatalogueDescription/'
            'gmd:featureCatalogueCitation',
            {'gmd': 'http://www.isotc211.org/2005/gmd'})):
            ci.attrib.pop('uuidref')
        md_metadata.xml = etree.tostring(tree)

        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_namespace(self, wfs, mp_remote_describefeaturetype):
        """Test the owsutil.get_namespace method.

        Test whether the namespace of the dov-pub:Boringen layer is correct.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.

        """
        assert owsutil.get_namespace(wfs, 'dov-pub:Boringen') == \
               'http://dov.vlaanderen.be/ocdov/dov-pub'

    def test_get_remote_featurecatalogue(self, mp_remote_fc):
        """Test the owsutil.get_remote_featurecatalogue method.

        Test whether the feature catalogue of the dov-pub:Boringen layer
        matches the format described in the docs.

        Parameters
        ----------
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue of the
            dov-pub:Boringen layer.

        """
        fc = owsutil.get_remote_featurecatalogue(
            'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
            'c0cbd397-520f-4ee1-aca7-d70e271eeed6')

        assert type(fc) is dict

        assert 'definition' in fc
        assert type(fc['definition']) in (str, unicode)

        assert 'attributes' in fc
        assert type(fc['attributes']) is dict

        attrs = fc['attributes']
        if len(attrs) > 0:
            for attr in attrs.values():
                assert type(attr) is dict

                assert 'definition' in attr
                assert type(attr['definition']) in (str, unicode)

                assert 'values' in attr
                assert type(attr['values']) is list
                if len(attr['values']) > 0:
                    for v in attr['values']:
                        assert type(v) in (str, unicode)
                    assert len(attr['values']) == len(set(attr['values']))

                assert 'multiplicity' in attr
                mp = attr['multiplicity']
                assert type(mp) is tuple
                assert len(mp) == 2
                assert mp[0] in (0, 1)
                assert (type(mp[1]) is int and mp[1] > 0) or mp[1] == 'Inf'

    def test_get_remote_featurecataloge_baduuid(self, mp_remote_fc_notfound):
        """Test the owsutil.get_remote_featurecatalogue method with an
        inexistent feature catalogue uuid.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        mp_remote_fc_notfound : pytest.fixture
            Monkeypatch the call to get an inexistent remote featurecatalogue.

        """
        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_remote_featurecatalogue(
                'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
                'badfc000-0000-0000-0000-badfc00badfc')

    def test_get_remote_metadata(self, md_metadata):
        """Test the owsutil.get_remote_metadata method.

        Test whether the resulting MD_Metadata is correct.

        Parameters
        ----------
        md_metadata : pytest.fixture returning owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        assert type(md_metadata) is MD_Metadata

    def test_get_remote_metadata_nometadataurls(self, wfs):
        """Test the owsutil.get_remote_metadata method when the WFS layer
        missed metadata URLs.

        Test whether a MetadataNotFoundError is raised.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contentmetadata = wfs.contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_remote_metadata(contentmetadata)
