"""Module grouping tests for the sondering search module."""
import datetime

import pandas as pd
import pytest

from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch
from pydov.search.sondering import SonderingSearch
from pydov.types.boring import Boring
from pydov.types.sondering import Sondering
from pydov.util import owsutil
from tests.abstract import (
    AbstractTestSearch,
)

from tests.test_search import (
    mp_wfs,
    wfs,
    mp_remote_md,
    mp_remote_fc,
    mp_remote_describefeaturetype,
    mp_remote_wfs_feature,
    mp_remote_xsd,
    mp_dov_xml,
    mp_dov_xml_broken,
    wfs_getfeature,
    wfs_feature,
)

location_md_metadata = 'tests/data/types/sondering/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/sondering/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/sondering/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/sondering/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/sondering/feature.xml'
location_dov_xml = 'tests/data/types/sondering/sondering.xml'
location_xsd_base = 'tests/data/types/sondering/xsd_*.xml'


@pytest.fixture
def md_metadata(wfs, mp_remote_md):
    """PyTest fixture providing a MD_Metadata instance of the
    dov-pub:Sonderingen layer.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    mp_remote_md : pytest.fixture
        Monkeypatch the call to get the remote metadata of the
        dov-pub:Sonderingen layer.

    Returns
    -------
    owslib.iso.MD_Metadata
        Parsed metadata describing the Sonderingen WFS layer in more detail,
        in the ISO 19115/19139 format.

    """
    contentmetadata = wfs.contents['dov-pub:Sonderingen']
    return owsutil.get_remote_metadata(contentmetadata)


class TestSonderingSearch(AbstractTestSearch):
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.boring.SonderingSearch
            Instance of SonderingSearch used for searching.

        """
        return SonderingSearch()

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.sondering.Sondering
            Class reference for the Sondering class.

        """
        return Sondering

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        return PropertyIsEqualTo(propertyname='sondeernummer',
                                 literal='GEO-61/3075-S1')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

    def get_xml_field(self):
        """Get the name of a field defined in XML only.

        Returns
        -------
        str
            The name of the XML field.

        """
        return 'gw_meting'

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_sondering', 'sondeernummer', 'diepte_sondering_tot',
                'datum_aanvang')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_sondering', 'sondeernummer', 'z', 'qc', 'Qt')

    def get_valid_returnfields_extra(self):
        """Get a list of valid return fields, including extra WFS only
        fields not present in the default dataframe.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.

        """
        return ('pkey_sondering', 'conus')

    def get_df_default_columns(self):
        """Get a list of the column names (and order) from the default
        dataframe.

        Returns
        -------
        list
            A list of the column names of the default dataframe.

        """
        return ['pkey_sondering', 'sondeernummer', 'x', 'y',
                'start_sondering_mtaw', 'diepte_sondering_van',
                'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
                'sondeermethode', 'apparaat', 'datum_gw_meting',
                'diepte_gw_m', 'z', 'qc', 'Qt', 'fs', 'u', 'i']

    def test_search_date(self, mp_wfs, mp_remote_describefeaturetype,
                         mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                         mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
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
        df = self.get_search_object().search(
            query=self.get_valid_query_single())

        # specific test for the Zulu time wfs 1.1.0 issue
        assert df.datum_aanvang.unique()[0] == datetime.date(2002, 12, 17)

        assert pd.Timestamp(
            df.datum_gw_meting.unique()[0]).to_pydatetime() == \
               datetime.datetime(2002, 12, 17, 14, 30, 0, 0)

    def test_search_nan(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                        mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
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
        df = self.get_search_object().search(
            query=self.get_valid_query_single())

        assert df.Qt.hasnans

    def test_search_xmlresolving(self, mp_remote_describefeaturetype,
                                 mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=('pkey_sondering', 'sondeernummer', 'diepte_gw_m'))

        assert df.diepte_gw_m[0] == 3.60
