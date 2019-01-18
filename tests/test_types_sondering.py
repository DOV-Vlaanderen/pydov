"""Module grouping tests for the pydov.types.sondering module."""

from pydov.types.sondering import Sondering
from tests.abstract import AbstractTestTypes

from tests.test_search_sondering import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml,
    location_wfs_getfeature,
    location_wfs_feature,
    location_dov_xml,
)

class TestSondering(AbstractTestTypes):
    """Class grouping tests for the pydov.types.sondering.Sondering class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.sondering.Sondering
            Class reference for the Sondering class.

        """
        return Sondering

    def get_namespace(self):
        """Get the WFS namespace associated with this datatype.

        Returns
        -------
        str
            WFS namespace for this type.

        """
        return 'http://dov.vlaanderen.be/ocdov/dov-pub'

    def get_pkey_base(self):
        """Get the base URL for the permanent keys of this datatype.

        Returns
        -------
        str
            Base URL for the permanent keys of this datatype. For example
            "https://www.dov.vlaanderen.be/data/sondering/"

        """
        return 'https://www.dov.vlaanderen.be/data/sondering/'

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list
            List of field names.

        """
        return ['pkey_sondering', 'sondeernummer', 'x', 'y',
                'start_sondering_mtaw', 'diepte_sondering_van',
                'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
                'sondeermethode', 'apparaat', 'datum_gw_meting',
                'diepte_gw_m', 'z', 'qc', 'Qt', 'fs', 'u', 'i']

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        return ['z', 'qc', 'Qt', 'fs', 'u', 'i']

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        return ['pkey_sondering', 'sondeernummer', 'x', 'y',
                'start_sondering_mtaw', 'diepte_sondering_van',
                'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
                'sondeermethode', 'apparaat', 'datum_gw_meting',
                'diepte_gw_m']

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_sondering', 'sondeernummer')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_sondering', 'sondeernummer', 'z')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

