"""Module grouping tests for the pydov.types.boring module."""
from collections import OrderedDict

import pytest
from numpy.compat import unicode
from owslib.etree import etree

import pydov
from pydov.types.boring import Boring
from pydov.util.errors import InvalidFieldError


@pytest.fixture
def mp_boring_xml(monkeypatch):
    def _get_xml_data(*args, **kwargs):
        with open('tests/data/types/boring/boring.xml', 'r') as f:
            data = f.read().encode('utf-8')
        return data

    monkeypatch.setattr(pydov.types.abstract.AbstractDovType,
                        '_get_xml_data', _get_xml_data)


class TestBoring(object):
    def test_get_field_names(self):
        fields = Boring.get_field_names()

        assert fields == ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                          'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                          'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                          'boorgatmeting', 'diepte_methode_van',
                          'diepte_methode_tot', 'boormethode']

    def test_get_field_names_nosubtypes(self):
        fields = Boring.get_field_names(return_fields=None,
                                        include_subtypes=False)

        assert fields == ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                          'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                          'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                          'boorgatmeting']

    def test_get_field_names_returnfields_nosubtypes(self):
        fields = Boring.get_field_names(return_fields=('pkey_boring',
                                                       'diepte_boring_tot'),
                                        include_subtypes=False)

        assert fields == ['pkey_boring', 'diepte_boring_tot']

    def test_get_field_names_wrongreturnfields(self):
        with pytest.raises(InvalidFieldError):
            Boring.get_field_names(return_fields=('pkey_boring',
                                                  'onbestaande'),
                                   include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        with pytest.raises(AttributeError):
            Boring.get_field_names(return_fields='pkey_boring',
                                   include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        with pytest.raises(InvalidFieldError):
            Boring.get_field_names(return_fields=['pkey_boring',
                                                  'boormethode'],
                                   include_subtypes=False)

    def test_get_fields(self):
        fields = Boring.get_fields()
        assert isinstance(fields, OrderedDict)

        for f in fields.keys():
            assert type(f) in (str, unicode)

            field = fields[f]
            assert type(field) is dict

            assert 'name' in field
            assert type(field['name']) in (str, unicode)
            assert field['name'] == f

            assert 'source' in field
            assert type(field['source']) in (str, unicode)
            assert field['source'] in ('wfs', 'xml')

            assert 'sourcefield' in field
            assert type(field['sourcefield']) in (str, unicode)

            assert 'type' in field
            assert type(field['type']) in (str, unicode)
            assert field['type'] in ['string', 'float', 'integer', 'date',
                                     'boolean']

            if field['source'] == 'wfs':
                assert 'definition' not in field
                assert 'notnull' not in field
            elif field['source'] == 'xml':
                assert 'definition' in field
                assert type(field['definition']) in (str, unicode)

                assert 'notnull' in field
                assert type(field['notnull']) is bool

    def test_get_fields_sourcewfs(self):
        fields = Boring.get_fields(source=('wfs',))
        for field in fields.values():
            assert field['source'] == 'wfs'

    def test_get_fields_sourcexml(self):
        fields = Boring.get_fields(source=('xml',))
        for field in fields.values():
            assert field['source'] == 'xml'

    def test_from_wfs_element(self):
        with open('tests/data/types/boring/feature.xml', 'r') as f:
            feature = etree.fromstring(f.read())

        boring = Boring.from_wfs_element(
            feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        assert type(boring) is Boring

    def test_get_df_array(self, mp_boring_xml):
        with open('tests/data/types/boring/feature.xml', 'r') as f:
            feature = etree.fromstring(f.read())

        boring = Boring.from_wfs_element(
            feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        df_array = boring.get_df_array()
        assert type(df_array) is list
        assert len(df_array) == 2

    def test_get_df_array_wrongreturnfields(self):
        with open('tests/data/types/boring/feature.xml', 'r') as f:
            feature = etree.fromstring(f.read())

        boring = Boring.from_wfs_element(
            feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        with pytest.raises(InvalidFieldError):
            boring.get_df_array(return_fields=('onbestaand',))
