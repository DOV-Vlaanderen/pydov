"""Module grouping tests for the pydov.types.boring module."""

from pydov.types.boring import Boring
from tests.abstract import AbstractTestTypes

from tests.test_search_boring import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml,
    location_wfs_getfeature,
    location_wfs_feature,
    location_dov_xml,
)

class TestBoring(AbstractTestTypes):
    """Class grouping tests for the pydov.types.boring.Boring class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.boring.Boring
            Class reference for the Boring class.

        """
        return Boring

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
            "https://www.dov.vlaanderen.be/data/boring/"

        """
        return 'https://www.dov.vlaanderen.be/data/boring/'

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list
            List of field names.

        """
        return ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                'boorgatmeting', 'diepte_methode_van',
                'diepte_methode_tot', 'boormethode']

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        return ['diepte_methode_van', 'diepte_methode_tot', 'boormethode']

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        return ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                'boorgatmeting']

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_boring', 'diepte_boring_tot')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_boring', 'diepte_methode_van', 'boormethode')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

