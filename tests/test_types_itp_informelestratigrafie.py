"""Module grouping tests for the
pydov.types.interpretaties.InformeleStratigrafie class."""
import pytest

from owslib.etree import etree
from pydov.types.interpretaties import InformeleStratigrafie
from pydov.util.errors import InvalidFieldError
from tests.abstract import AbstractTestTypes

from tests.test_search_itp_informelestratigrafie import (
    wfs_feature,
    wfs_getfeature,
    mp_dov_xml,
    location_wfs_feature,
    location_wfs_getfeature,
    location_dov_xml,
)


class TestInformeleStratigrafie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.InformeleStratigrafie class."""

    def test_get_field_names(self):
        """Test the InformeleStratigrafie.get_field_names method.

        Tests whether the available fields for the InformeleStratigrafie type
        match the ones we list in docs/description_output_dataframes.rst.

        """
        fields = InformeleStratigrafie.get_field_names()

        assert fields == ['pkey_interpretatie', 'pkey_boring',
                          'pkey_sondering', 'betrouwbaarheid_interpretatie',
                          'diepte_laag_van', 'diepte_laag_tot', 'beschrijving']

    def test_get_field_names_nosubtypes(self):
        """Test the InformeleStratigrafie.get_field_names method without
        including subtypes.

        Tests whether the fields provided in a subtype are not listed when
        disabling subtypes.

        """
        fields = InformeleStratigrafie.get_field_names(return_fields=None,
                                                       include_subtypes=False)

        assert fields == ['pkey_interpretatie', 'pkey_boring',
                          'pkey_sondering', 'betrouwbaarheid_interpretatie']

    def test_get_field_names_returnfields_nosubtypes(self):
        """Test the InformeleStratigrafie.get_field_names method when
        specifying return fields.

        Tests whether the returned fields match the ones provided as return
        fields.
        """
        fields = InformeleStratigrafie.get_field_names(
            return_fields=('pkey_interpretatie', 'pkey_boring'),
            include_subtypes=False)

        assert fields == ['pkey_interpretatie', 'pkey_boring']

    def test_get_field_names_returnfields_order(self):
        """Test the InformeleStratigrafie.get_field_names method when
        specifying return fields in a different order.

        Tests whether the returned fields match the ones provided as return
        fields and that the order is the one we list in
        docs/description_output_dataframes.rst.

        """
        fields = InformeleStratigrafie.get_field_names(
            return_fields=(
                'betrouwbaarheid_interpretatie', 'pkey_interpretatie'),
            include_subtypes=False)

        assert fields == ['pkey_interpretatie',
                          'betrouwbaarheid_interpretatie']

    def test_get_field_names_wrongreturnfields(self):
        """Test the InformeleStratigrafie.get_field_names method when
        specifying an inexistent return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            InformeleStratigrafie.get_field_names(
                return_fields=('pkey_interpretatie', 'onbestaande'),
                include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        """Test the InformeleStratigrafie.get_field_names method when listing
        a single return field instead of a list.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            InformeleStratigrafie.get_field_names(
                return_fields='pkey_interpretatie', include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the InformeleStratigrafie.get_field_names method when
        disabling subtypes and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            InformeleStratigrafie.get_field_names(
                return_fields=['pkey_interpretatie', 'diepte_laag_van'],
                include_subtypes=False)

    def test_get_fields(self):
        """Test the InformeleStratigrafie.get_fields method.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        """
        fields = InformeleStratigrafie.get_fields()
        self.abstract_test_get_fields(fields)

    def test_get_fields_nosubtypes(self):
        """Test the InformeleStratigrafie.get_fields method not including
        subtypes.

        Test whether fields provides by subtypes are not listed in the output.

        """
        fields = InformeleStratigrafie.get_fields(include_subtypes=False)
        for field in fields:
            assert field not in ('diepte_laag_van', 'diepte_laag_tot',
                                 'beschrijving')

    def test_from_wfs_element(self, wfs_feature):
        """Test the InformeleStratigrafie.from_wfs_element method.

        Test whether we can construct a Boring instance from a WFS
        response element.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        itp = InformeleStratigrafie.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        assert type(itp) is InformeleStratigrafie

        assert itp.pkey.startswith(
            'https://www.dov.vlaanderen.be/data/interpretatie/')
        assert itp.typename == 'interpretatie'
        assert type(itp.data) is dict
        assert type(itp.subdata) is dict

    def test_get_df_array(self, wfs_feature, mp_dov_xml):
        """Test the InformeleStratigrafie.get_df_array method.

        Test whether the output of the dataframe array for the given
        InformeleStratigrafie is correct.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        itp = InformeleStratigrafie.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        fields = [f for f in InformeleStratigrafie.get_fields(
            source=('wfs', 'xml', 'custom')).values() if not f.get(
            'wfs_injected', False)]

        df_array = itp.get_df_array()
        self.abstract_test_get_df_array(df_array, fields)

    def test_get_df_array_wrongreturnfields(self, wfs_feature):
        """Test the InformeleStratigrafie.get_df_array specifying a
        nonexistent return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        itp = InformeleStratigrafie.from_wfs_element(
            wfs_feature, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        with pytest.raises(InvalidFieldError):
            itp.get_df_array(return_fields=('onbestaand',))

    def test_from_wfs_str(self, wfs_getfeature):
        """Test the InformeleStratigrafie.from_wfs method to construct
        InformeleStratigrafie objects from a WFS response, as str.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the layer.

        """
        itps = InformeleStratigrafie.from_wfs(
            wfs_getfeature, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        for itp in itps:
            assert type(itp) is InformeleStratigrafie

    def test_from_wfs_bytes(self, wfs_getfeature):
        """Test the InformeleStratigrafie.from_wfs method to construct
        InformeleStratigrafie objects from a WFS response, as bytes.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the layer.

        """
        itps = InformeleStratigrafie.from_wfs(
            wfs_getfeature.encode('utf-8'),
            'http://dov.vlaanderen.be/ocdov/interpretaties')

        for itp in itps:
            assert type(itp) is InformeleStratigrafie

    def test_from_wfs_tree(self, wfs_getfeature):
        """Test the InformeleStratigrafie.from_wfs method to construct
        InformeleStratigrafie objects from a WFS response, as elementtree.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the layer.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        itps = InformeleStratigrafie.from_wfs(
            tree, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        for itp in itps:
            assert type(itp) is InformeleStratigrafie

    def test_from_wfs_list(self, wfs_getfeature):
        """Test the InformeleStratigrafie.from_wfs method to construct
        InformeleStratigrafie objects from a WFS response, as list of elements.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response of the layer.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        feature_members = tree.findall('.//{http://www.opengis.net/gml}'
                                        'featureMembers')

        itps = InformeleStratigrafie.from_wfs(
            feature_members, 'http://dov.vlaanderen.be/ocdov/interpretaties')

        for itp in itps:
            assert type(itp) is InformeleStratigrafie
