"""Module grouping tests for the pydov.types.boring module."""
from collections import OrderedDict

import datetime
import pytest
from numpy.compat import unicode
from owslib.etree import etree

import pydov
from pydov.types.boring import Boring
from pydov.util.errors import InvalidFieldError


@pytest.fixture
def mp_boring_xml(monkeypatch):
    """Monkeypatch the call to get the remote Boring XML data.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """

    def _get_xml_data(*args, **kwargs):
        with open('tests/data/types/boring/boring.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.types.abstract.AbstractDovType,
                        '_get_xml_data', _get_xml_data)


@pytest.fixture
def wfs_feature():
    """PyTest fixture providing an XML of a WFS feature element of a Boring
    record.

    Returns
    -------
    etree.Element
        XML element representing a single record of the Boring WFS layer.

    """
    with open('tests/data/types/boring/feature.xml', 'r') as f:
        return etree.fromstring(f.read())


class TestBoring(object):
    """Class grouping tests for the pydov.types.boring.Boring class."""

    def test_get_field_names(self):
        """Test the Boring.get_field_names method.

        Tests whether the available fields for the Boring type match the
        ones we list in docs/description_output_dataframes.rst.

        """
        fields = Boring.get_field_names()

        assert fields == ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                          'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                          'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                          'boorgatmeting', 'diepte_methode_van',
                          'diepte_methode_tot', 'boormethode']

    def test_get_field_names_nosubtypes(self):
        """Test the Boring.get_field_names method without including subtypes.

        Tests whether the fields provided in a subtype are not listed when
        disabling subtypes.

        """
        fields = Boring.get_field_names(return_fields=None,
                                        include_subtypes=False)

        assert fields == ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                          'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                          'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                          'boorgatmeting']

    def test_get_field_names_returnfields_nosubtypes(self):
        """Test the Boring.get_field_names method when specifying return
        fields.

        Tests whether the returned fields match the ones provided as return
        fields.
        """
        fields = Boring.get_field_names(return_fields=('pkey_boring',
                                                       'diepte_boring_tot'),
                                        include_subtypes=False)

        assert fields == ['pkey_boring', 'diepte_boring_tot']

    def test_get_field_names_returnfields_order(self):
        """Test the Boring.get_field_names method when specifying return
        fields in a different order.

        Tests whether the returned fields match the ones provided as return
        fields and that the order is the one we list in
        docs/description_output_dataframes.rst.

        """
        fields = Boring.get_field_names(
            return_fields=('diepte_boring_tot', 'pkey_boring'),
            include_subtypes=False)

        assert fields == ['pkey_boring', 'diepte_boring_tot']

    def test_get_field_names_wrongreturnfields(self):
        """Test the Boring.get_field_names method when specifying an
        inexistent return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            Boring.get_field_names(return_fields=('pkey_boring',
                                                  'onbestaande'),
                                   include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        """Test the Boring.get_field_names method when listing a single
        return field instead of a list.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            Boring.get_field_names(return_fields='pkey_boring',
                                   include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the Boring.get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            Boring.get_field_names(return_fields=['pkey_boring',
                                                  'boormethode'],
                                   include_subtypes=False)

    def test_get_fields(self):
        """Test the Boring.get_fields method.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        """
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
                assert sorted(field.keys()) == [
                    'name', 'source', 'sourcefield', 'type']
            elif field['source'] == 'xml':
                assert 'definition' in field
                assert type(field['definition']) in (str, unicode)

                assert 'notnull' in field
                assert type(field['notnull']) is bool

                assert sorted(field.keys()) == [
                    'definition', 'name', 'notnull', 'source', 'sourcefield',
                    'type']

    def test_get_fields_sourcewfs(self):
        """Test the Boring.get_fields method for fields of the WFS source.

        Test whether all returned fields have 'wfs' as their 'source'.

        """
        fields = Boring.get_fields(source=('wfs',))
        for field in fields.values():
            assert field['source'] == 'wfs'

    def test_get_fields_sourcexml(self):
        """Test the Boring.get_fields method for fields of the XML source.

        Test whether all returned fields have 'xml' as their 'source'.

        """
        fields = Boring.get_fields(source=('xml',))
        for field in fields.values():
            assert field['source'] == 'xml'

    def test_get_fields_nosubtypes(self):
        """Test the Boring.get_fields method not including subtypes.

        Test whether fields provides by subtypes are not listed in the output.

        """
        fields = Boring.get_fields(include_subtypes=False)
        for field in fields:
            assert field not in ('diepte_methode_van',
                                 'diepte_methode_tot', 'boormethode')

    def test_from_wfs_element(self, wfs_feature):
        """Test the Boring.from_wfs_element method.

        Test whether we can construct a Boring instance from a WFS
        response element.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the Boring WFS layer.

        """
        boring = Boring.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        assert type(boring) is Boring

    def test_get_df_array(self, wfs_feature, mp_boring_xml):
        """Test the boring.get_df_array method.

        Test whether the output of the dataframe array for the given Boring
        is correct.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the Boring WFS layer.
        mp_boring_xml : pytest.fixture
            Monkeypatch the call to get the remote Boring XML data.

        """
        boring = Boring.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        fields = Boring.get_fields()

        df_array = boring.get_df_array()
        assert type(df_array) is list
        assert len(df_array) == 2

        for record in df_array:
            assert len(record) == len(fields)

            for value, field in zip(record, fields.values()):
                if field['type'] == 'string':
                    assert type(value) in (str, unicode)
                elif field['type'] == 'float':
                    assert type(value) is float or value is None
                elif field['type'] == 'integer':
                    assert type(value) is int or value is None
                elif field['type'] == 'date':
                    assert type(value) is datetime.date or value is None
                elif field['type'] == 'boolean':
                    assert type(value) is bool or value is None

                if field['name'] == 'pkey_boring':
                    assert value.startswith(
                        'https://www.dov.vlaanderen.be/data/boring/')
                    assert not value.endswith('.xml')

    def test_get_df_array_wrongreturnfields(self, wfs_feature):
        """Test the boring.get_df_array specifying a nonexistent return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the Boring WFS layer.

        """
        boring = Boring.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/dov-pub')

        with pytest.raises(InvalidFieldError):
            boring.get_df_array(return_fields=('onbestaand',))
