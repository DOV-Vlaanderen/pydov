"""Module grouping tests for the pydov.util.owsutil module."""

import pickle

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
from tests import network_services_enabled

test_namespace_data = [
    ('dov-pub:Boringen', 'http://dov.vlaanderen.be/ocdov/dov-pub'),
    ('gw_meetnetten:meetnetten',
     'http://dov.vlaanderen.be/grondwater/gw_meetnetten')
]

fc_uuids = ('c0cbd397-520f-4ee1-aca7-d70e271eeed6',  # Boringen
            'b142965f-b2aa-429e-86ff-a7cb0e065d48')  # Grondwatermeetnetten
test_remote_fc_data = list(zip(
    ['https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw']*len(fc_uuids),
    fc_uuids
))


@pytest.fixture
def wfs():
    return WebFeatureService(
        url="https://www.dov.vlaanderen.be/geoserver/wfs",
        version="1.1.0")


class TestOwsutil(object):
    def test_get_csw_base_url(self):
        with open('tests/data/util/owsutil/contentmetadata.py2.pickle',
                  'rb') as f:
            contentmetadata = pickle.load(f)
            assert owsutil.get_csw_base_url(contentmetadata) == \
                   'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw'

    def test_get_csw_base_url_nometadataurls(self):
        with open('tests/data/util/owsutil/contentmetadata.py2.pickle',
                  'rb') as f:
            contentmetadata = pickle.load(f)
            contentmetadata.metadataUrls = []
            with pytest.raises(MetadataNotFoundError):
                owsutil.get_csw_base_url(contentmetadata)

    def test_get_featurecatalogue_uuid(self):
        with open('tests/data/util/owsutil/md_metadata.py2.pickle', 'rb') as f:
            md_metadata = pickle.load(f)
            assert owsutil.get_featurecatalogue_uuid(md_metadata) == \
                   'c0cbd397-520f-4ee1-aca7-d70e271eeed6'

    def test_get_featurecatalogue_uuid_nocontentinfo(self):
        with open('tests/data/util/owsutil/md_metadata.py2.pickle', 'rb') as f:
            md_metadata = pickle.load(f)
            tree = etree.fromstring(md_metadata.xml)
            root = tree.find('{http://www.isotc211.org/2005/gmd}MD_Metadata')
            for ci in tree.findall(
                    './/{http://www.isotc211.org/2005/gmd}contentInfo'):
                root.remove(ci)
            md_metadata.xml = etree.tostring(tree)

            with pytest.raises(FeatureCatalogueNotFoundError):
                owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_featurecatalogue_uuid_nouuidref(self):
        with open('tests/data/util/owsutil/md_metadata.py2.pickle', 'rb') as f:
            md_metadata = pickle.load(f)
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

    @pytest.mark.skipif(not network_services_enabled,
                        reason="not testing network services")
    @pytest.mark.parametrize("layer,namespace", test_namespace_data)
    def test_get_namespace(self, wfs, layer, namespace):
        assert owsutil.get_namespace(wfs, layer) == namespace

    @pytest.mark.skipif(not network_services_enabled,
                        reason="not testing network services")
    @pytest.mark.parametrize("csw_url,fc_uuid", test_remote_fc_data)
    def test_get_remote_featurecatalogue(self, csw_url, fc_uuid):
        fc = owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

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

    @pytest.mark.skipif(not network_services_enabled,
                        reason="not testing network services")
    def test_get_remote_featurecataloge_baduuid(self):
        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_remote_featurecatalogue(
                'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
                'badfc000-0000-0000-0000-badfc00badfc')

    @pytest.mark.skipif(not network_services_enabled,
                        reason="not testing network services")
    def test_get_remote_metadata(self):
        with open('tests/data/util/owsutil/contentmetadata.py2.pickle',
                  'rb') as f:
            contentmetadata = pickle.load(f)

            md_metadata = owsutil.get_remote_metadata(contentmetadata)
            assert type(md_metadata) is MD_Metadata

    def test_get_remote_metadata_exception(self):
        with open('tests/data/util/owsutil/contentmetadata.py2.pickle',
                  'rb') as f:
            contentmetadata = pickle.load(f)
            contentmetadata.metadataUrls = []
            with pytest.raises(MetadataNotFoundError):
                owsutil.get_remote_metadata(contentmetadata)
