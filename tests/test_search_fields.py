"""Class grouping tests for the fields module."""

import pytest
from pydov.search.fields import AbstractReturnField, GeometryReturnField, ReturnField, ReturnFieldList, FieldMetadataList, FieldMetadata


class TestReturnFieldList():
    """Test the ReturnFieldList class."""

    def _test_from_field_names(self, field_names):
        """Helper method to test the from_field_names method.

        Parameters
        ----------
        field_names : any
            Field names used in the from_field_names method.
        """
        rfl = ReturnFieldList.from_field_names(
            field_names
        )

        assert isinstance(rfl, ReturnFieldList)

        for rf in rfl:
            assert isinstance(rf, AbstractReturnField)

        rf_names = [rf.name for rf in rfl]
        assert [f for f in field_names if f not in rf_names] == []

    def test_from_field_names_list(self):
        """Test the from_field_names method with a list of strings."""
        self._test_from_field_names(
            ['field1', 'field2']
        )

    def test_from_field_names_set(self):
        """Test the from_field_names method with a set of strings."""
        self._test_from_field_names(
            set(['field1', 'field2'])
        )

    def test_from_field_names_tuple(self):
        """Test the from_field_names method with a tuple of strings."""
        self._test_from_field_names(
            ('field1', 'field2')
        )

    def test_from_field_names_none(self):
        """Test the from_field_names method without specifying field names."""
        assert ReturnFieldList.from_field_names(None) is None
        assert ReturnFieldList.from_field_names() is None

    def test_from_field_names_parameters(self):
        """Test the from_field_names method with two string parameters."""
        rfl = ReturnFieldList.from_field_names(
            'field1', 'field2'
        )

        assert isinstance(rfl, ReturnFieldList)

        for rf in rfl:
            assert isinstance(rf, AbstractReturnField)

        rf_names = [rf.name for rf in rfl]
        assert [f for f in ('field1', 'field2') if f not in rf_names] == []

    def test_from_field_names_single_parameter(self):
        """Test the from_field_names method with a single string parameter."""
        rfl = ReturnFieldList.from_field_names(
            'field1'
        )

        assert isinstance(rfl, ReturnFieldList)

        for rf in rfl:
            assert isinstance(rf, AbstractReturnField)

        rf_names = [rf.name for rf in rfl]
        assert [f for f in ('field1',) if f not in rf_names] == []

    def test_get_names(self):
        """Test the get_names method."""
        rfl = ReturnFieldList.from_field_names('field1', 'field2')
        assert rfl.get_names() == ['field1', 'field2']

    def test_contains(self):
        """Test whether the contains check works with field names."""
        rfl = ReturnFieldList.from_field_names('field1', 'field2')

        assert 'field1' in rfl
        assert 'field3' not in rfl


class TestReturnField():
    """Class grouping tests for the ReturnField class."""

    def test_initialise(self):
        """Test initialisation of a ReturnField."""
        rf = ReturnField('field1')
        assert isinstance(rf, ReturnField)

    def test_name(self):
        """Test whether the name of the ReturnField is accessible."""
        rf = ReturnField('field1')
        assert rf.name == 'field1'


class TestGeometryReturnField():
    """Class grouping tests for the GeometryReturnField class."""

    def test_no_srs(self):
        """Test initialisation of a GeometryReturnField without an SRS.

        Test whether a TypeError is raised.
        """
        with pytest.raises(TypeError):
            GeometryReturnField('shape')

    def test_srs_31370(self):
        """Test initialisation of a GeometryReturnField with CRS set to Belgian Lambert 72."""
        rf = GeometryReturnField('shape', 31370)

        assert isinstance(rf, GeometryReturnField)
        assert rf.name == 'shape'
        assert rf.epsg == 31370

    def test_wrong_srs_type(self):
        """Test initialisation of a GeometryReturnField with a wrong CRS type.

        Test whether a TypeError is raised.
        """
        with pytest.raises(TypeError):
            GeometryReturnField('shape', 'EPSG:31370')

    def test_wrong_srs_value(self):
        """Test initialisation of a GeometryReturnField with a wrong CRS type.

        Test whether a TypeError is raised.
        """
        with pytest.raises(ValueError):
            GeometryReturnField('shape', 404000)


class TestFieldMetadata():
    """Class grouping tests for the FieldMetadata class."""

    def test_initialise(self):
        """Test initialisation of a FieldMetadata."""
        fm = FieldMetadata({
            'name': 'field1',
            'datatype': 'string',
            'source': 'wfs'
        })
        assert isinstance(fm, FieldMetadata)
        assert fm.name == 'field1'
        assert fm.datatype == 'string'
        assert fm.source == 'wfs'


class TestFieldMetadataList():
    """Class grouping tests for the FieldMetadataList class."""

    def test_initialise(self):
        """Test initialisation of a FieldMetadataList."""
        fml = FieldMetadataList()
        assert isinstance(fml, FieldMetadataList)

    def test_add(self):
        """Test adding FieldMetadata instances to a FieldMetadataList."""
        fml = FieldMetadataList()

        fm1 = FieldMetadata({
            'name': 'field1',
            'datatype': 'string',
            'source': 'wfs'
        })
        fm2 = FieldMetadata({
            'name': 'field2',
            'datatype': 'float',
            'source': 'xml'
        })

        fml.add(fm1)
        fml.add(fm2)

        assert len(fml) == 2
        assert isinstance(fml['field1'], FieldMetadata)
        assert isinstance(fml['field2'], FieldMetadata)
        assert fml['field1'].name == 'field1'
        assert fml['field2'].name == 'field2'
