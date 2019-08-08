"""Module grouping tests for the boring search module."""

import pytest

from pydov.types.boring import Boring
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.types.interpretaties import (
    GecodeerdeLithologie,
    HydrogeologischeStratigrafie,
    InformeleStratigrafie,
    LithologischeBeschrijvingen,
    FormeleStratigrafie,
    GeotechnischeCodering,
    QuartairStratigrafie,
)
from pydov.types.sondering import Sondering

type_objects = [Boring,
                Sondering,
                GrondwaterFilter,
                InformeleStratigrafie,
                FormeleStratigrafie,
                HydrogeologischeStratigrafie,
                GecodeerdeLithologie,
                LithologischeBeschrijvingen,
                GeotechnischeCodering,
                QuartairStratigrafie,]


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
        {'name': 'grondwatersysteem',
         'source': 'xml',
         'sourcefield': '/filter/ligging/grondwatersysteem',
         'definition': 'Grondwatersysteem waarin de filter hangt.',
         'type': 'string',
         'notnull': False
         }
    ]

    fields = objecttype.extend_fields(extra_fields)

    assert len(fields) == len(objecttype.fields) + len(extra_fields)

    assert fields[-1] == extra_fields[-1]
