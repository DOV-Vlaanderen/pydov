"""Module grouping tests for the pydov.types.boring module."""
import numpy as np
from collections import OrderedDict

import datetime
import pytest
from numpy.compat import unicode
from pandas.core.dtypes.common import is_object_dtype

from owslib.etree import etree

from pydov.types.boring import Boring
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.errors import InvalidFieldError
from tests.abstract import AbstractTestTypes

from tests.test_search_grondwaterfilter import (
    wfs_getfeature,
    wfs_feature,
    mp_dov_xml
)


class TestGrondwaterFilter(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""

    def test_get_field_names(self):
        """Test the GrondwaterFilter.get_field_names method.

        Tests whether the available fields for the Boring type match the
        ones we list in docs/description_output_dataframes.rst.

        """
        fields = GrondwaterFilter.get_field_names()

        assert fields == ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                          'filternummer', 'filtertype', 'x', 'y', 'mv_mtaw',
                          'gemeente', 'meetnet_code', 'aquifer_code',
                          'grondwaterlichaam_code', 'regime',
                          'diepte_onderkant_filter', 'lengte_filter',
                          'datum', 'tijdstip', 'peil_mtaw',
                          'betrouwbaarheid', 'methode']

    def test_get_field_names_nosubtypes(self):
        """Test the Boring.get_field_names method without including subtypes.

        Tests whether the fields provided in a subtype are not listed when
        disabling subtypes.

        """
        fields = GrondwaterFilter.get_field_names(return_fields=None,
                                                  include_subtypes=False)

        assert fields == ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                          'filternummer', 'filtertype', 'x', 'y', 'mv_mtaw',
                          'gemeente', 'meetnet_code', 'aquifer_code',
                          'grondwaterlichaam_code', 'regime',
                          'diepte_onderkant_filter', 'lengte_filter']

    def test_get_field_names_returnfields_nosubtypes(self):
        """Test the Boring.get_field_names method when specifying return
        fields.

        Tests whether the returned fields match the ones provided as return
        fields.
        """
        fields = GrondwaterFilter.get_field_names(
            return_fields=('pkey_filter', 'meetnet_code'),
            include_subtypes=False)

        assert fields == ['pkey_filter', 'meetnet_code']

    def test_get_field_names_returnfields_order(self):
        """Test the Boring.get_field_names method when specifying return
        fields in a different order.

        Tests whether the returned fields match the ones provided as return
        fields and that the order is the one we list in
        docs/description_output_dataframes.rst.

        """
        fields = GrondwaterFilter.get_field_names(
            return_fields=('meetnet_code', 'pkey_filter'),
            include_subtypes=False)

        assert fields == ['pkey_filter', 'meetnet_code']

    def test_get_field_names_wrongreturnfields(self):
        """Test the Boring.get_field_names method when specifying an
        inexistent return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            GrondwaterFilter.get_field_names(
                return_fields=('pkey_filter', 'onbestaande'),
                include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        """Test the Boring.get_field_names method when listing a single
        return field instead of a list.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            GrondwaterFilter.get_field_names(
                return_fields='pkey_filter', include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the Boring.get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            GrondwaterFilter.get_field_names(
                return_fields=['pkey_filter', 'peil_mtaw'],
                include_subtypes=False)

    def test_get_fields(self):
        """Test the Boring.get_fields method.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        """
        fields = GrondwaterFilter.get_fields()
        self.abstract_test_get_fields(fields)

    def test_get_fields_nosubtypes(self):
        """Test the Boring.get_fields method not including subtypes.

        Test whether fields provides by subtypes are not listed in the output.

        """
        fields = GrondwaterFilter.get_fields(include_subtypes=False)
        for field in fields:
            assert field not in ('datum', 'tijdstip', 'peil_mtaw',
                                 'betrouwbaarheid', 'methode')

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
        grondwaterfilter = GrondwaterFilter.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        assert type(grondwaterfilter) is GrondwaterFilter

        assert grondwaterfilter.pkey.startswith(
            'https://www.dov.vlaanderen.be/data/filter/')
        assert grondwaterfilter.typename == 'grondwaterfilter'
        assert type(grondwaterfilter.data) is dict
        assert type(grondwaterfilter.subdata) is dict

    def test_get_df_array(self, wfs_feature, mp_dov_xml):
        """Test the boring.get_df_array method.

        Test whether the output of the dataframe array for the given Boring
        is correct.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the Boring WFS layer.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote Boring XML data.

        """
        grondwaterfilter = GrondwaterFilter.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        fields = [f for f in GrondwaterFilter.get_fields().values()
                  if not f.get('wfs_injected', False)]

        df_array = grondwaterfilter.get_df_array()
        self.abstract_test_get_df_array(df_array, fields)

    def test_get_df_array_wrongreturnfields(self, wfs_feature):
        """Test the boring.get_df_array specifying a nonexistent return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the Boring WFS layer.

        """
        grondwaterfilter = GrondwaterFilter.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        with pytest.raises(InvalidFieldError):
            grondwaterfilter.get_df_array(return_fields=('onbestaand',))

    def test_from_wfs_str(self, wfs_getfeature):
        """Test the boring.from_wfs method to construct Boring objects from
        a WFS response, as str.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the
            dov-pub:Boringen layer.

        """
        grondwaterfilters = GrondwaterFilter.from_wfs(
            wfs_getfeature,
            'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        for grondwaterfilter in grondwaterfilters:
            assert type(grondwaterfilter) is GrondwaterFilter

    def test_from_wfs_bytes(self, wfs_getfeature):
        """Test the boring.from_wfs method to construct Boring objects from
        a WFS response, as bytes.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the
            dov-pub:Boringen layer.

        """
        grondwaterfilters = GrondwaterFilter.from_wfs(
            wfs_getfeature.encode('utf-8'),
            'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        for grondwaterfilter in grondwaterfilters:
            assert type(grondwaterfilter) is GrondwaterFilter

    def test_from_wfs_tree(self, wfs_getfeature):
        """Test the boring.from_wfs method to construct Boring objects from
        a WFS response, as elementtree.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the
            dov-pub:Boringen layer.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        grondwaterfilters = GrondwaterFilter.from_wfs(
            tree, 'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        for grondwaterfilter in grondwaterfilters:
            assert type(grondwaterfilter) is GrondwaterFilter

    def test_from_wfs_list(self, wfs_getfeature):
        """Test the boring.from_wfs method to construct Boring objects from
        a WFS response, as list of elements.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the
            dov-pub:Boringen layer.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        feature_members = tree.findall('.//{http://www.opengis.net/gml}'
                                        'featureMembers')

        grondwaterfilters = GrondwaterFilter.from_wfs(
            feature_members,
            'http://dov.vlaanderen.be/grondwater/gw_meetnetten')

        for grondwaterfilter in grondwaterfilters:
            assert type(grondwaterfilter) is GrondwaterFilter
