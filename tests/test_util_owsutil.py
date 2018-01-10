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
def wfs(monkeypatch):
    def read(*args, **kwargs):
        with open('tests/data/util/owsutil/wfscapabilities.xml', 'r') as f:
            data = etree.fromstring(f.read().encode('utf-8'))
        return data

    monkeypatch.setattr(
        owslib.feature.common.WFSCapabilitiesReader, 'read', read)

    return WebFeatureService(
        url="https://www.dov.vlaanderen.be/geoserver/wfs",
        version="1.1.0")


@pytest.fixture
def md_metadata(wfs, monkeypatch):
    def openURL(*args, **kwargs):
        class Io:
            def read(*args, **kwargs):
                from numpy.compat import unicode
                with open('tests/data/util/owsutil/md_metadata.xml', 'r') as f:
                    data = f.read()
                    if type(data) is unicode:
                        data = data.encode('utf-8')
                return data
        return Io()

    if sys.version_info[0] < 3:
        monkeypatch.setattr('owslib.util.openURL.func_code', openURL.func_code)
    else:
        monkeypatch.setattr('owslib.util.openURL.__code__', openURL.__code__)

    contentmetadata = wfs.contents['dov-pub:Boringen']
    return owsutil.get_remote_metadata(contentmetadata)


@pytest.fixture
def mp_remote_fc(monkeypatch):
    def openURL(*args, **kwargs):
        class Io:
            def read(*args, **kwargs):
                from numpy.compat import unicode
                with open(
                    'tests/data/util/owsutil/fc_featurecatalogue.xml',
                        'r') as f:
                    data = f.read()
                    if type(data) is unicode:
                        data = data.encode('utf-8')
                return data
        return Io()

    if sys.version_info[0] < 3:
        monkeypatch.setattr('owslib.util.openURL.func_code', openURL.func_code)
    else:
        monkeypatch.setattr('owslib.util.openURL.__code__', openURL.__code__)


@pytest.fixture
def mp_remote_fc_notfound(monkeypatch):
    def openURL(*args, **kwargs):
        class Io:
            def read(*args, **kwargs):
                with open(
                    'tests/data/util/owsutil/fc_featurecatalogue_notfound.xml',
                        'r') as f:
                    data = f.read().encode('utf-8')
                return data
        return Io()

    if sys.version_info[0] < 3:
        monkeypatch.setattr('owslib.util.openURL.func_code', openURL.func_code)
    else:
        monkeypatch.setattr('owslib.util.openURL.__code__', openURL.__code__)

@pytest.fixture
def mp_remote_describefeaturetype(monkeypatch):
    def openURL(*args, **kwargs):
        class Io:
            def read(*args, **kwargs):
                with open(
                    'tests/data/util/owsutil/wfsdescribefeaturetype.xml',
                        'r') as f:
                    data = f.read().encode('utf-8')
                return data
        return Io()

    if sys.version_info[0] < 3:
        monkeypatch.setattr('owslib.util.openURL.func_code', openURL.func_code)
    else:
        monkeypatch.setattr('owslib.util.openURL.__code__', openURL.__code__)


class TestOwsutil(object):
    def test_get_csw_base_url(self, wfs):
        contentmetadata = wfs.contents['dov-pub:Boringen']
        assert owsutil.get_csw_base_url(contentmetadata) == \
               'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw'

    def test_get_csw_base_url_nometadataurls(self, wfs):
        contentmetadata = wfs.contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_csw_base_url(contentmetadata)

    def test_get_featurecatalogue_uuid(self, md_metadata):
        assert owsutil.get_featurecatalogue_uuid(md_metadata) == \
               'c0cbd397-520f-4ee1-aca7-d70e271eeed6'

    def test_get_featurecatalogue_uuid_nocontentinfo(self, md_metadata):
        tree = etree.fromstring(md_metadata.xml)
        root = tree.find('{http://www.isotc211.org/2005/gmd}MD_Metadata')
        for ci in tree.findall(
                './/{http://www.isotc211.org/2005/gmd}contentInfo'):
            root.remove(ci)
        md_metadata.xml = etree.tostring(tree)

        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_featurecatalogue_uuid_nouuidref(self, md_metadata):
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
        assert owsutil.get_namespace(wfs, 'dov-pub:Boringen') == \
               'http://dov.vlaanderen.be/ocdov/dov-pub'

    def test_get_remote_featurecatalogue(self, mp_remote_fc):
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
        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_remote_featurecatalogue(
                'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
                'badfc000-0000-0000-0000-badfc00badfc')

    def test_get_remote_metadata(self, md_metadata):
        assert type(md_metadata) is MD_Metadata

    def test_get_remote_metadata_exception(self, wfs):
        contentmetadata = wfs.contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_remote_metadata(contentmetadata)
