"""Module grouping tests for the boring search module."""

import pytest

from pydov.types.bodemsite import Bodemsite
from pydov.types.bodemlocatie import Bodemlocatie
from pydov.types.bodemdiepteinterval import Bodemdiepteinterval
from pydov.types.bodemobservatie import Bodemobservatie
from pydov.types.bodemmonster import Bodemmonster
from pydov.types.bodemclassificatie import Bodemclassificatie
from pydov.types.boring import Boring
from pydov.types.fields import XmlField
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.types.grondwatermonster import GrondwaterMonster
from pydov.types.grondmonster import Grondmonster
from pydov.types.interpretaties import (
    GecodeerdeLithologie,
    HydrogeologischeStratigrafie,
    InformeleStratigrafie,
    LithologischeBeschrijvingen,
    FormeleStratigrafie,
    GeotechnischeCodering,
    QuartairStratigrafie,
    InformeleHydrogeologischeStratigrafie,
)
from pydov.types.sondering import Sondering


type_objects = [Bodemsite,
                Bodemlocatie,
                Bodemdiepteinterval,
                Bodemobservatie,
                Bodemmonster,
                Bodemclassificatie,
                Boring,
                Sondering,
                GrondwaterFilter,
                GrondwaterMonster,
                InformeleStratigrafie,
                FormeleStratigrafie,
                HydrogeologischeStratigrafie,
                InformeleHydrogeologischeStratigrafie,
                GecodeerdeLithologie,
                LithologischeBeschrijvingen,
                GeotechnischeCodering,
                QuartairStratigrafie,
                Grondmonster]


@pytest.mark.parametrize("objecttype", type_objects)
def test_get_fields_sourcewfs(objecttype):
    """Test the get_fields method for fields of the WFS source.

    Test whether all returned fields have 'wfs' as their 'source'.

    """
    fields = objecttype.get_fields(source=('wfs',))
    for field in fields.values():
        assert field['source'] == 'wfs'


@pytest.mark.parametrize("objecttype", type_objects)
def test_get_fields_sourcexml(objecttype):
    """Test the Boring.get_fields method for fields of the XML source.

    Test whether all returned fields have 'xml' as their 'source'.

    """
    fields = objecttype.get_fields(source=('xml',))
    for field in fields.values():
        assert field['source'] == 'xml'


@pytest.mark.parametrize("objecttype", type_objects)
def test_get_fields_subtypes_notnull(objecttype):
    """Test the get_fields method for fields of the subtype.

    Test whether all returned fields have 'notnull' = False.

    Fields of a subtype cannot be mandatory since the subtype itself is not
    compulsory.

    """
    allfields = objecttype.get_field_names()
    ownfields = objecttype.get_field_names(include_subtypes=False)
    subfields = [f for f in allfields if f not in ownfields]

    fields = objecttype.get_fields(source=('xml',))
    for field in fields.values():
        if field['name'] in subfields:
            assert field['notnull'] is False


@pytest.mark.parametrize("objecttype", type_objects)
def test_extend_fields_no_extra(objecttype):
    """Test the extend_fields method for empty extra_fields.

    Test whether the returned fields match the existing fields.
    Test whether the returned fields are not the same fields as the original
    fields.

    """
    fields = objecttype.extend_fields([])
    assert fields == objecttype.fields
    assert fields is not objecttype.fields


@pytest.mark.parametrize("objecttype", type_objects)
def test_extend_fields_with_extra(objecttype):
    """Test the extend_fields method with extra_fields.

    Test whether the extra field is included.

    """
    extra_fields = [
        XmlField(name='grondwatersysteem',
                 source_xpath='/filter/ligging/grondwatersysteem',
                 definition='Grondwatersysteem waarin de filter hangt.',
                 datatype='string',
                 notnull=False)
    ]

    fields = objecttype.extend_fields(extra_fields)

    assert len(fields) == len(objecttype.fields) + len(extra_fields)

    assert fields[-1] == extra_fields[-1]
