"""Module grouping tests for the search grondwaterfilter module."""
import datetime

from owslib.fes import PropertyIsEqualTo
from pydov.search.grondwaterlocatie import GrondwaterLocatieSearch
from pydov.types.grondwaterlocatie import GrondwaterLocatie
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

location_md_metadata = 'tests/data/types/grondwaterlocatie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterlocatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterlocatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/grondwaterlocatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterlocatie/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterlocatie/grondwaterlocatie.xml'
location_xsd_base = 'tests/data/types/grondwaterlocatie/xsd_*.xml'


class TestGrondwaterlocatieSearch(AbstractTestSearch):
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.grondwaterlocatie.GrondwaterLocatieSearch
            Instance of GrondwaterLocatieSearch used for searching.

        """
        return GrondwaterLocatieSearch()

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.grondwaterlocatie.GrondwaterLocatie
            Class reference for the GrondwaterLocatie class.

        """
        return GrondwaterLocatie

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        return PropertyIsEqualTo(
            propertyname='putfiche',
            literal='https://www.dov.vlaanderen.be/data/put/2019-019725')

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
        return 'mv_mtaw'

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_grondwaterlocatie', 'gw_id')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_grondwaterlocatie', 'gw_id', 'beheerder')

    def get_valid_returnfields_extra(self):
        """Get a list of valid return fields, including extra WFS only
        fields not present in the default dataframe.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.

        """
        return ('pkey_grondwaterlocatie', 'gw_id', 'aquifer')

    def get_df_default_columns(self):
        """Get a list of the column names (and order) from the default
        dataframe.

        Returns
        -------
        list
            A list of the column names of the default dataframe.

        """
        return ['pkey_grondwaterlocatie', 'gw_id', 'x', 'y', 'mv_mtaw',
                'start_grondwaterlocatie_mtaw', 'gemeente',
                'beheerder_vanaf', 'beheerder_tot', 'beheerder']

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
            return_fields=('pkey_grondwaterlocatie', 'gw_id', 'mv_mtaw'))

        assert df.mv_mtaw[0] == 11.82
