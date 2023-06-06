"""Module grouping tests for the pydov.types.bodemdiepteinterval module."""

from pydov.types.bodemdiepteinterval import Bodemdiepteinterval
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemdiepteinterval/' \
    'wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemdiepteinterval/feature.xml'


class TestBodemdiepteinterval(AbstractTestTypes):
    """Class grouping tests for the 
    pydov.types.bodemdiepteinterval.Bodemdiepteinterval class."""

    datatype_class = Bodemdiepteinterval
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemdiepteinterval/')

    field_names = [
        'pkey_diepteinterval', 'pkey_bodemopbouw', 'pkey_bodemlocatie',
        'nr', 'type', 'naam', 'bovengrens1_cm', 'bovengrens2_cm',
        'ondergrens1_cm', 'ondergrens2_cm', 'ondergrens_bereikt',
        'grensduidelijkheid', 'grensregelmatigheid', 'beschrijving', 'x', 'y',
        'mv_mtaw']
    field_names_subtypes = []
    field_names_nosubtypes = [
        'pkey_diepteinterval', 'pkey_bodemopbouw', 'pkey_bodemlocatie',
        'nr', 'type', 'naam', 'bovengrens1_cm', 'bovengrens2_cm',
        'ondergrens1_cm', 'ondergrens2_cm', 'ondergrens_bereikt',
        'grensduidelijkheid', 'grensregelmatigheid', 'beschrijving', 'x', 'y',
        'mv_mtaw']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_diepteinterval', 'naam')
    valid_returnfields_subtype = None

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemdiepteinterval has no subtypes.
        """
        assert True
