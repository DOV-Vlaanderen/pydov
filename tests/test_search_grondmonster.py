"""Module grouping tests for the search grondmonster module."""
import datetime

from owslib.fes import PropertyIsEqualTo
from pydov.search.grondmonster import GrondmonsterSearch
from pydov.types.grondmonster import Grondmonster
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

location_md_metadata = 'tests/data/types/grondmonster/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondmonster/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondmonster/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondmonster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondmonster/feature.xml'
location_dov_xml = 'tests/data/types/grondmonster/grondmonster.xml'
location_xsd_base = 'tests/data/types/grondmonster/xsd_*.xml'


class TestGrondmonsterSearch(AbstractTestSearch):
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.grondmonster.GrondmonsterSearch
            Instance of GrondmonsterSearch used for searching.

        """
        return GrondmonsterSearch()

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.grondmonster.Grondmonster
            Class reference for the Grondmonster class.

        """
        return Grondmonster

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        return PropertyIsEqualTo(propertyname='boornummer',
                                 literal='GEO-04/024-B6')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

    def get_wfs_field(self):
        """Get the name of a WFS field.

        Returns
        -------
        str
            The name of the WFS field.

        """
        return 'boornummer'

    def get_xml_field(self):
        """Get the name of a field defined in XML only.

        Returns
        -------
        str
            The name of the XML field.

        """
        return 'astm_naam'

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_grondmonster', 'boornummer')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_grondmonster', 'boornummer', 'diameter')

    def get_valid_returnfields_extra(self):
        """Get a list of valid return fields, including extra WFS only
        fields not present in the default dataframe.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.

        """
        return ('pkey_grondmonster', 'korrelverdeling')

    def get_df_default_columns(self):
        """Get a list of the column names (and order) from the default
        dataframe.

        Returns
        -------
        list
            A list of the column names of the default dataframe.

        """
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
                'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
                'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
                'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
                'uitrolgrens', 'vloeigrens', 'glauconiet',
                'korrelvolumemassa', 'volumemassa', 'watergehalte',
                'diameter', 'fractie', 'methode']

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
            return_fields=('pkey_grondmonster', 'boornummer', 'humusgehalte',
                           'methode'))

        assert df.humusgehalte[0] == 15.6
        assert df.methode[22] == 'AREOMETER'
