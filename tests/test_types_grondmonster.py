"""Module grouping tests for the pydov.types.grondmonster module."""

from pydov.types.grondmonster import Grondmonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

from tests.test_search_grondmonster import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml,
    location_wfs_getfeature,
    location_wfs_feature,
    location_dov_xml,
)

class TestGrondmonster(AbstractTestTypes):
    """Class grouping tests for the pydov.types.grondmonster.Grondmonster class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.grondmonster.Grondmonster
            Class reference for the Grondmonster class.

        """
        return Grondmonster

    def get_namespace(self):
        """Get the WFS namespace associated with this datatype.

        Returns
        -------
        str
            WFS namespace for this type.

        """
        return 'http://dov.vlaanderen.be/ocdov/boringen'

    def get_pkey_base(self):
        """Get the base URL for the permanent keys of this datatype.

        Returns
        -------
        str
            Base URL for the permanent keys of this datatype. For example
            "https://www.dov.vlaanderen.be/data/grondmonster/"

        """
        return build_dov_url('data/grondmonster/')

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list
            List of field names.

        """
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
                'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
                'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
                'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
                'uitrolgrens', 'vloeigrens', 'glauconiet',
                'korrelvolumemassa', 'volumemassa', 'watergehalte',
                'diameter', 'fractie', 'methode']

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
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
                'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
                'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
                'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
                'uitrolgrens', 'vloeigrens', 'glauconiet',
                'korrelvolumemassa', 'volumemassa', 'watergehalte']

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_grondmonster', 'diepte_tot_m')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('diameter', 'fractie', 'methode')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

