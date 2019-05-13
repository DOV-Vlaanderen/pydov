"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.grondwaterfilter import GrondwaterFilter
from tests.abstract import AbstractTestTypes

from tests.test_search_grondwaterfilter import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml,
    location_wfs_getfeature,
    location_wfs_feature,
    location_dov_xml,
)


class TestGrondwaterFilter(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.grondwaterfilter.GrondwaterFilter
            Class reference for the GrondwaterFilter class.

        """
        return GrondwaterFilter

    def get_namespace(self):
        """Get the WFS namespace associated with this datatype.

        Returns
        -------
        str
            WFS namespace for this type.

        """
        return 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'

    def get_pkey_base(self):
        """Get the base URL for the permanent keys of this datatype.

        Returns
        -------
        str
            Base URL for the permanent keys of this datatype. For example
            "https://www.dov.vlaanderen.be/data/boring/"

        """
        return 'https://www.dov.vlaanderen.be/data/filter/'

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list
            List of field names.

        """
        return ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                'filternummer', 'filtertype', 'x', 'y', 'mv_mtaw',
                'gemeente', 'meetnet_code', 'aquifer_code',
                'grondwaterlichaam_code', 'regime',
                'diepte_onderkant_filter', 'lengte_filter',
                'datum', 'tijdstip', 'peil_mtaw',
                'betrouwbaarheid', 'methode']

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        return ['datum', 'tijdstip', 'peil_mtaw', 'betrouwbaarheid',
                'methode']

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        return ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                'filternummer', 'filtertype', 'x', 'y', 'mv_mtaw',
                'gemeente', 'meetnet_code', 'aquifer_code',
                'grondwaterlichaam_code', 'regime',
                'diepte_onderkant_filter', 'lengte_filter']

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_filter', 'meetnet_code')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_filter', 'peil_mtaw')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'
