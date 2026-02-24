"""Module grouping tests for the search grondwaterfilter module."""
import pytest

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.search.fields import ReturnFieldList
from pydov.types.grondwaterfilter import GrondwaterFilter, Gxg
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/grondwaterfilter_gxg/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterfilter_gxg/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterfilter_gxg/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondwaterfilter_gxg/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter_gxg/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter_gxg/grondwaterfilter.xml'
location_codelists = 'tests/data/types/grondwaterfilter_gxg'


@pytest.mark.skip("GxG not available in production")
class TestGrondwaterfilterGxgSearch(AbstractTestSearch):

    search_instance = GrondwaterFilterSearch(objecttype=GrondwaterFilter.with_subtype(Gxg))
    search_class = GrondwaterFilterSearch
    datatype_class = GrondwaterFilter.with_subtype(Gxg)

    valid_query_single = PropertyIsEqualTo(propertyname='filterfiche',
                                           literal=build_dov_url(
                                               'data/filter/1996-011637'))

    inexistent_field = 'onbestaand'
    wfs_field = 'filternummer'
    xml_field = 'gxg_jaar'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_filter', 'filternummer')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_filter', 'filternummer', 'gxg_jaar')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_filter', 'beheerder')

    df_default_columns = ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                          'filternummer', 'filtertype', 'x', 'y',
                          'start_grondwaterlocatie_mtaw', 'mv_mtaw',
                          'gemeente', 'meetnet_code', 'aquifer_code',
                          'grondwaterlichaam_code', 'regime',
                          'diepte_onderkant_filter', 'lengte_filter',
                          'gxg_jaar', 'gxg_hg3', 'gxg_lg3', 'gxg_vg3']

    def test_search_gxg(self, mp_wfs, mp_get_schema,
                        mp_remote_describefeaturetype, mp_remote_md,
                        mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single)

        assert df.gxg_jaar.iloc[0] == 1996
        assert df.gxg_hg3.iloc[0] == 57.85
        assert df.gxg_lg3.iloc[0] == 57.01
        assert df.gxg_vg3.iloc[0] == 57.55
