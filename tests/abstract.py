import datetime
import re

import numpy as np
from collections import OrderedDict

import pandas as pd
import pytest
import requests
from numpy.compat import (
    unicode,
    long,
)
from pandas import DataFrame
from pandas.api.types import (
    is_int64_dtype, is_object_dtype,
    is_bool_dtype, is_float_dtype)

from owslib.fes import PropertyIsEqualTo
from owslib.etree import etree
from pydov.util.errors import InvalidFieldError
from pydov.util.location import (
    Within,
    Box,
)


def service_ok(url='https://www.dov.vlaanderen.be/geoserver', timeout=5):
    """Check whether the given URL is accessible.

    Used to skip online tests when the service is unavailable or unreachable.

    Parameters
    ----------
    url : str, optional
        The URL to test. Defaults to the DOV Geoserver.
    timeout : int, optional
        Timeout in seconds. Defaults to 5.

    Returns
    -------
    bool
        True if the service is reachable, False otherwise.

    """
    try:
        ok = requests.get(url, timeout=timeout).ok
    except requests.exceptions.ReadTimeout:
        ok = False
    except requests.exceptions.ConnectTimeout:
        ok = False
    except Exception:
        ok = False
    return ok


def clean_xml(xml):
    """Clean the given XML string of namespace definition, namespace
    prefixes and syntactical but otherwise meaningless differences.

    Parameters
    ----------
    xml : str
        String representation of XML document.

    Returns
    -------
    str
        String representation of cleaned XML document.

    """
    # remove xmlns namespace definitions
    r = re.sub(r'[ ]+xmlns:[^=]+="[^"]+"', '', xml)

    # remove namespace prefixes in tags
    r = re.sub(r'<(/?)[^:]+:([^ >]+)([ >])', r'<\1\2\3', r)

    # remove extra spaces in tags
    r = re.sub(r'[ ]+/>', '/>', r)

    # remove extra spaces between tags
    r = re.sub(r'>[ ]+<', '><', r)

    return r


class AbstractTestSearch(object):
    """Class grouping common test code for search classes."""
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.abstract.AbstractSearch
            Instance of subclass of this type used for searching.

        """
        raise NotImplementedError

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.abstract.AbstractDovType
            Class reference for the corresponding datatype.

        """
        raise NotImplementedError

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        raise NotImplementedError

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        raise NotImplementedError

    def get_xml_field(self):
        """Get the name of a field defined in XML only.

        Returns
        -------
        str
            The name of the XML field.

        """
        raise NotImplementedError

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        raise NotImplementedError

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        raise NotImplementedError

    def get_valid_returnfields_extra(self):
        """Get a list of valid return fields, including extra WFS only
        fields not present in the default dataframe.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.

        """
        raise NotImplementedError

    def get_df_default_columns(self):
        """Get a list of the column names (and order) from the default
        dataframe.

        Returns
        -------
        list
            A list of the column names of the default dataframe.

        """
        raise NotImplementedError

    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, mp_remote_xsd):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.

        """
        fields = self.get_search_object().get_fields()

        assert type(fields) is dict

        for field in fields:
            assert type(field) in (str, unicode)

            f = fields[field]
            assert type(f) is dict

            assert 'name' in f
            assert type(f['name']) in (str, unicode)
            assert f['name'] == field

            assert 'definition' in f
            assert type(f['name']) in (str, unicode)

            assert 'type' in f
            assert type(f['type']) in (str, unicode)
            assert f['type'] in ['string', 'float', 'integer', 'date',
                                 'datetime', 'boolean']

            assert 'notnull' in f
            assert type(f['notnull']) is bool

            assert 'query' in f
            assert type(f['query']) is bool

            assert 'cost' in f
            assert type(f['cost']) is int
            assert f['cost'] > 0

            if 'values' in f:
                assert sorted(f.keys()) == [
                    'cost', 'definition', 'name', 'notnull', 'query', 'type',
                    'values']

                assert type(f['values']) is dict

                for v in f['values'].keys():
                    assert type(f['values'][v]) in (str, unicode) or f[
                        'values'][v] is None

                    if f['type'] == 'string':
                        assert type(v) in (str, unicode)
                    elif f['type'] == 'float':
                        assert type(v) is float
                    elif f['type'] == 'integer':
                        assert type(v) is int
                    elif f['type'] == 'date':
                        assert type(v) is datetime.date
                    elif f['type'] == 'boolean':
                        assert type(v) is bool
            else:
                assert sorted(f.keys()) == ['cost', 'definition', 'name',
                                            'notnull', 'query', 'type']

    def test_search_both_location_query(self, mp_remote_describefeaturetype,
                                        mp_remote_wfs_feature):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.get_search_object().search(
            location=Within(Box(1, 2, 3, 4)),
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields())

        assert type(df) is DataFrame

    def test_search(self, mp_wfs, mp_remote_describefeaturetype, mp_remote_md,
                    mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single())

        assert type(df) is DataFrame

        assert list(df) == self.get_df_default_columns()

        datatype = self.get_type()
        allfields = datatype.get_field_names()
        ownfields = datatype.get_field_names(include_subtypes=False)
        subfields = [f for f in allfields if f not in ownfields]

        assert len(df) >= 1

        for field in list(df):
            if field in ownfields:
                assert len(df[field].unique()) == 1
            elif field in subfields:
                assert len(df[field].unique()) >= 1

        # dtype checks of the resulting df columns
        fields = self.get_search_object().get_fields()

        for field in list(df):
            mandatory = fields[field]['notnull']
            if mandatory:
                assert len(df[field]) == len(df[field].dropna())

        for field in list(df):
            field_datatype = fields[field]['type']
            datatypes = set((type(i) for i in df[field].dropna()))
            assert len(datatypes) <= 1

            if len(datatypes) > 0:
                if field_datatype == 'string':
                    assert str in datatypes
                elif field_datatype == 'float':
                    assert float in datatypes
                elif field_datatype == 'integer':
                    # in Python2 Panda's int64 dtype is translated into 'long'
                    assert (int in datatypes or long in datatypes)
                elif field_datatype == 'date':
                    assert datetime.date in datatypes
                elif field_datatype == 'boolean':
                    assert bool in datatypes

    def test_search_returnfields(self, mp_remote_wfs_feature):
        """Test the search method with the query parameter and a selection of
        return fields.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields())

        assert type(df) is DataFrame

        assert list(df) == list(self.get_valid_returnfields())

    def test_search_returnfields_subtype(self, mp_remote_wfs_feature):
        """Test the search method with the query parameter and a selection of
        return fields, including fields from a subtype.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields_subtype())

        assert type(df) is DataFrame

        assert list(df) == list(self.get_valid_returnfields_subtype())

    def test_search_returnfields_order(self, mp_remote_wfs_feature):
        """Test the search method with the query parameter and a selection of
        return fields in another ordering.

        Test whether the output dataframe contains only the selected return
        fields, in the order that is documented in
        docs/description_output_dataframes.rst

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields()[::-1])

        assert type(df) is DataFrame

        assert list(df) == list(self.get_valid_returnfields())

    def test_search_wrongreturnfields(self):
        """Test the search method with the query parameter and an inexistent
        return field.

        Test whether an InvalidFieldError is raised.

        """
        return_fields = list(self.get_valid_returnfields())
        return_fields.append(self.get_inexistent_field())

        with pytest.raises(InvalidFieldError):
            self.get_search_object().search(
                query=self.get_valid_query_single(),
                return_fields=return_fields)

    def test_search_wrongreturnfieldstype(self):
        """Test the search method with the query parameter and a single
        return field as string.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            self.get_search_object().search(
                query=self.get_valid_query_single(),
                return_fields=self.get_valid_returnfields()[0])

    def test_search_query_wrongfield(self):
        """Test the search method with the query parameter using an
        inexistent query field.

        Test whether an InvalidFieldError is raised.

        """
        query = PropertyIsEqualTo(propertyname=self.get_inexistent_field(),
                                  literal='The cat is out of the bag.')

        with pytest.raises(InvalidFieldError):
            self.get_search_object().search(
                query=query)

    def test_search_query_wrongfield_returnfield(self):
        """Test the search method with the query parameter using an
        return-only field as query field.

        Test whether an InvalidFieldError is raised.

        """
        query = PropertyIsEqualTo(propertyname=self.get_xml_field(),
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            self.get_search_object().search(query=query)

    def test_search_extrareturnfields(self, mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with the query parameter and an extra WFS
        field as return field.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields_extra())

        assert type(df) is DataFrame

        assert list(df) == list(self.get_valid_returnfields_extra())

    def test_search_xml_noresolve(self, mp_remote_describefeaturetype,
                                  mp_remote_wfs_feature, mp_dov_xml_broken):
        """Test the search method with return fields from WFS only.

        Test whether no XML is resolved.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml_broken : pytest.fixture
            Monkeypatch the call to break fetching of remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=self.get_valid_returnfields_extra())

    def test_get_fields_xsd_values(self, mp_remote_xsd):
        """Test the result of get_fields when the XML field has an XSD type.

        Test whether the output from get_fields() returns the values from
        the XSD.

        Parameters
        ----------
        mp_remote_xsd : pytest.fixture
            Monkeypatch the call to get XSD schemas.

        """
        xsd_schemas = self.get_type().get_xsd_schemas()

        if len(xsd_schemas) > 0:
            xml_fields = self.get_type().get_fields(source='xml')
            fields = self.get_search_object().get_fields()
            for f in xml_fields.values():
                if 'xsd_type' in f:
                    assert 'values' in fields[f['name']]
                    assert type(fields[f['name']]['values']) is dict

    def test_get_fields_no_xsd(self):
        """Test whether no XML fields have an XSD type when no XSD schemas
        are available."""
        xsd_schemas = self.get_type().get_xsd_schemas()

        if len(xsd_schemas) == 0:
            xml_fields = self.get_type().get_fields(source='xml')
            for f in xml_fields.values():
                assert 'xsd_type' not in f

    def test_get_fields_xsd_enums(self):
        """Test whether at least one XML field has an XSD type when there
        are XSD schemas available.

        Make sure XSD schemas are only listed (and downloaded) when they are
        needed.

        """
        xsd_schemas = self.get_type().get_xsd_schemas()

        xsd_type_count = 0

        if len(xsd_schemas) > 0:
            xml_fields = self.get_type().get_fields(source='xml')
            for f in xml_fields.values():
                if 'xsd_type' in f:
                    xsd_type_count += 1
            assert xsd_type_count > 0


class AbstractTestTypes(object):
    """Class grouping common test code for datatype classes."""
    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.abstract.AbstractDovType
            Class reference for the corresponding datatype.

        """
        raise NotImplementedError

    def get_namespace(self):
        """Get the WFS namespace associated with this datatype.

        Returns
        -------
        str
            WFS namespace for this type.

        """
        raise NotImplementedError

    def get_pkey_base(self):
        """Get the base URL for the permanent keys of this datatype.

        Returns
        -------
        str
            Base URL for the permanent keys of this datatype. For example
            "https://www.dov.vlaanderen.be/data/boring/"

        """
        raise NotImplementedError

    def get_field_names(self):
        """Get the field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst

        Returns
        -------
        list<str>
            List of field names.

        """
        raise NotImplementedError

    def get_field_names_subtypes(self):
        """Get the field names of this type that originate from subtypes only.

        Returns
        -------
        list<str>
            List of field names from subtypes.

        """
        raise NotImplementedError

    def get_field_names_nosubtypes(self):
        """Get the field names for this type, without including fields from
        subtypes.

        Returns
        -------
        list<str>
            List of field names.

        """
        raise NotImplementedError

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        raise NotImplementedError

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        raise NotImplementedError

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        raise NotImplementedError

    def test_get_field_names(self):
        """Test the get_field_names method.

        Tests whether the available fields for the type match the
        ones we list in docs/description_output_dataframes.rst.

        """
        fields = self.get_type().get_field_names()
        assert fields == self.get_field_names()

    def test_get_field_names_nosubtypes(self):
        """Test the get_field_names method without including subtypes.

        Tests whether the fields provided in a subtype are not listed when
        disabling subtypes.

        """
        fields = self.get_type().get_field_names(
            return_fields=None, include_subtypes=False)

        assert fields == self.get_field_names_nosubtypes()

    def test_get_field_names_returnfields_nosubtypes(self):
        """Test the get_field_names method when specifying return
        fields.

        Tests whether the returned fields match the ones provided as return
        fields.

        """
        fields = self.get_type().get_field_names(
            return_fields=self.get_valid_returnfields(),
            include_subtypes=False)

        assert fields == list(self.get_valid_returnfields())

    def test_get_field_names_returnfields_order(self):
        """Test the get_field_names method when specifying return
        fields in a different order.

        Tests whether the returned fields match the ones provided as return
        fields and that the order is the one we list in
        docs/description_output_dataframes.rst.

        """
        fields = self.get_type().get_field_names(
            return_fields=self.get_valid_returnfields()[::-1],
            include_subtypes=False)

        assert fields == list(self.get_valid_returnfields())

    def test_get_field_names_wrongreturnfields(self):
        """Test the get_field_names method when specifying an
        inexistent return field.

        Test whether an InvalidFieldError is raised.

        """
        return_fields = list(self.get_valid_returnfields())
        return_fields.append(self.get_inexistent_field())

        with pytest.raises(InvalidFieldError):
            self.get_type().get_field_names(
                return_fields=return_fields,
                include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        """Test the get_field_names method when listing a single
        return field instead of a list.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            self.get_type().get_field_names(
                return_fields=self.get_valid_returnfields()[0],
                include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        """
        with pytest.raises(InvalidFieldError):
            self.get_type().get_field_names(
                return_fields=self.get_valid_returnfields_subtype(),
                include_subtypes=False)

    def test_get_fields(self):
        """Test the get_fields method.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        """
        fields = self.get_type().get_fields()

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
                                     'datetime', 'boolean']

            if field['source'] == 'wfs':
                if 'wfs_injected' in field.keys():
                    assert sorted(field.keys()) == [
                        'name', 'source', 'sourcefield', 'type',
                        'wfs_injected']
                else:
                    assert sorted(field.keys()) == [
                        'name', 'source', 'sourcefield', 'type']
            elif field['source'] == 'xml':
                assert 'definition' in field
                assert type(field['definition']) in (str, unicode)

                assert 'notnull' in field
                assert type(field['notnull']) is bool

                if 'xsd_type' in field:
                    assert sorted(field.keys()) == [
                        'definition', 'name', 'notnull', 'source',
                        'sourcefield', 'type', 'xsd_type']
                else:
                    assert sorted(field.keys()) == [
                        'definition', 'name', 'notnull', 'source',
                        'sourcefield', 'type']

    def test_get_fields_nosubtypes(self):
        """Test the get_fields method not including subtypes.

        Test whether fields provides by subtypes are not listed in the output.

        """
        fields = self.get_type().get_fields(include_subtypes=False)
        for field in fields:
            assert field not in self.get_field_names_subtypes()

    def test_from_wfs_element(self, wfs_feature):
        """Test the from_wfs_element method.

        Test whether we can construct an instance from a WFS response element.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        feature = self.get_type().from_wfs_element(
            wfs_feature, self.get_namespace())

        assert type(feature) is self.get_type()

        assert feature.pkey.startswith(self.get_pkey_base())

        assert feature.pkey.startswith(
            'https://www.dov.vlaanderen.be/data/%s/' %
            feature.typename)

        assert type(feature.data) is dict
        assert type(feature.subdata) is dict

    def test_get_df_array(self, wfs_feature, mp_dov_xml):
        """Test the get_df_array method.

        Test whether the output of the dataframe array is correct.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        feature = self.get_type().from_wfs_element(
            wfs_feature, self.get_namespace())

        fields = [f for f in self.get_type().get_fields(
            source=('wfs', 'xml', 'custom')).values() if not
            f.get('wfs_injected', False)]

        df_array = feature.get_df_array()

        assert type(df_array) is list

        for record in df_array:
            assert len(record) == len(fields)

            for value, field in zip(record, fields):
                if field['type'] == 'string':
                    assert type(value) in (str, unicode) or np.isnan(value)
                elif field['type'] == 'float':
                    assert type(value) is float or np.isnan(value)
                elif field['type'] == 'integer':
                    assert type(value) is int or np.isnan(value)
                elif field['type'] == 'date':
                    assert type(value) is datetime.date or np.isnan(value)
                elif field['type'] == 'boolean':
                    assert type(value) is bool or np.isnan(value)

                if field['name'].startswith('pkey') and not pd.isnull(value):
                    assert value.startswith(
                        'https://www.dov.vlaanderen.be/data/')
                    assert not value.endswith('.xml')

    def test_get_df_array_wrongreturnfields(self, wfs_feature):
        """Test the get_df_array specifying a nonexistent return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        feature = self.get_type().from_wfs_element(
            wfs_feature, self.get_namespace())

        with pytest.raises(InvalidFieldError):
            feature.get_df_array(return_fields=(self.get_inexistent_field(),))

    def test_from_wfs_str(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as str.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response.

        """
        features = self.get_type().from_wfs(wfs_getfeature,
                                            self.get_namespace())

        for feature in features:
            assert type(feature) is self.get_type()

    def test_from_wfs_bytes(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as bytes.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response.

        """
        features = self.get_type().from_wfs(wfs_getfeature.encode('utf-8'),
                                            self.get_namespace())

        for feature in features:
            assert type(feature) is self.get_type()

    def test_from_wfs_tree(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as elementtree.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        features = self.get_type().from_wfs(tree, self.get_namespace())

        for feature in features:
            assert type(feature) is self.get_type()

    def test_from_wfs_list(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as list of elements.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returing str
            Fixture providing a WFS GetFeature response.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        feature_members = tree.findall('.//{http://www.opengis.net/gml}'
                                       'featureMembers')

        features = self.get_type().from_wfs(feature_members,
                                            self.get_namespace())

        for feature in features:
            assert type(feature) is self.get_type()
