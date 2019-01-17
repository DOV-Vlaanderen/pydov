"""Module grouping tests for the
pydov.types.interpretaties.FormeleStratigrafie class."""
from pydov.types.interpretaties import FormeleStratigrafie
from tests.abstract import AbstractTestTypes

from tests.test_search_itp_formelestratigrafie import (
    wfs_feature,
    wfs_getfeature,
    mp_dov_xml,
    location_wfs_feature,
    location_wfs_getfeature,
    location_dov_xml,
)


class TestFormeleStratigrafie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.FormeleStratigrafie class."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.interpretaties.FormeleStratigrafie
            Class reference for the FormeleStratigrafie class.

        """
        return FormeleStratigrafie

    def get_namespace(self):
        """Get the WFS namespace associated with this datatype.

        Returns
        -------
        str
            WFS namespace for this type.

        """
        return 'http://dov.vlaanderen.be/ocdov/interpretaties'

    def get_pkey_base(self):
        """Get the base URL for the permanent keys of this datatype.

        Returns
        -------
        str
            Base URL for the permanent keys of this datatype. For example
            "https://www.dov.vlaanderen.be/data/interpretatie/"

        """
        return 'https://www.dov.vlaanderen.be/data/interpretatie/'

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list
            List of field names.

        """
        return ['pkey_interpretatie', 'pkey_boring',
                'pkey_sondering', 'betrouwbaarheid_interpretatie', 'x', 'y',
                'diepte_laag_van', 'diepte_laag_tot', 'lid1', 'relatie_lid1_lid2', 'lid2']

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        return ['diepte_laag_van', 'diepte_laag_tot', 'lid1', 'relatie_lid1_lid2', 'lid2']

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        return ['pkey_interpretatie', 'pkey_boring',
                'pkey_sondering', 'betrouwbaarheid_interpretatie', 'x', 'y']

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_interpretatie', 'pkey_sondering')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'
