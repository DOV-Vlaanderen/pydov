"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.grondwatermonster import GrondwaterMonster
from tests.abstract import AbstractTestTypes

from tests.test_search_grondwaterfilter import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml,
    location_wfs_getfeature,
    location_wfs_feature,
    location_dov_xml,
)


class TestGrondwaterMonster(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.grondwatermonster.GrondwaterMonster
            Class reference for the GrondwaterMonster class.

        """
        return GrondwaterMonster

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
        return 'https://www.dov.vlaanderen.be/data/watermonster/'

    def get_field_names(self):
        """Get the field names for this type

        Returns
        -------
        list
            List of field names.

        """
        return [
            'pkey_grondwatermonster',
            'grondwatermonsternummer',
            'pkey_grondwaterlocatie',
            'pkey_filter',
            'gw_id',
            'filternummer',
            'x',
            'y',
            'mv_mtaw',
            'gemeente',
            'datum_monstername',
            'parameter',
            'eenheid',
            'detectie',
            'waarde',
            'parametergroep',
            'veld_labo'
        ]

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        return [
            'parameter',
            'eenheid',
            'detectie',
            'waarde',
            'parametergroep',
            'veld_labo'
        ]

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        return [
            'pkey_grondwatermonster',
            'grondwatermonsternummer',
            'pkey_grondwaterlocatie',
            'pkey_filter',
            'gw_id',
            'filternummer',
            'x',
            'y',
            'mv_mtaw',
            'gemeente',
            'datum_monstername',
        ]

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('gemeente', 'y')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_filter', 'pkey_grondwatermonster', 'eenheid')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'
