import datetime
import random
import re
from collections import OrderedDict

import numpy as np
import pandas as pd
import pytest
import requests
from owslib.etree import etree
from owslib.fes2 import PropertyIsEqualTo, SortBy, SortProperty
from pandas import DataFrame

import pydov
from pydov.types.abstract import AbstractField
from pydov.types.fields import ReturnField, ReturnFieldList
from pydov.util.dovutil import build_dov_url
from pydov.util.errors import InvalidFieldError
from pydov.util.location import Box, Within
from pydov.util.query import AbstractJoin, Join, PropertyInList


class ServiceCheck:

    is_service_ok = None

    @staticmethod
    def service_ok(timeout=5):
        """Check whether DOV services are accessible.

        Used to skip online tests when the service is unavailable or
        unreachable.

        Parameters
        ----------
        timeout : int, optional
            Timeout in seconds. Defaults to 5.

        Returns
        -------
        bool
            True if the DOV services are reachable, False otherwise.

        """
        def check_url(url, timeout):
            try:
                ok = pydov.session.head(
                    url, allow_redirects=True, timeout=timeout).ok
            except requests.exceptions.ReadTimeout:
                ok = False
            except requests.exceptions.ConnectTimeout:
                ok = False
            except Exception:
                ok = False
            return ok

        if ServiceCheck.is_service_ok is None:
            ServiceCheck.is_service_ok = (
                check_url(build_dov_url('geonetwork'), timeout) and
                check_url(build_dov_url('geoserver'), timeout) and
                check_url(
                    build_dov_url('xdov/schema/latest/xsd/kern/dov.xsd'),
                    timeout))

        return ServiceCheck.is_service_ok


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

    # remove namespace prefixes in attributes
    while re.match(r'<([^ >]+)( [^:]+ )*[^:]+:([^ >]+)([ >])', r):
        r = re.sub(r'<([^ >]+)( [^:]+ )*[^:]+:([^ >]+)([ >])', r'<\1\2\3\4', r)

    # remove extra spaces in tags
    r = re.sub(r'[ ]+/>', '/>', r)

    # remove extra spaces between tags
    r = re.sub(r'>[ ]+<', '><', r)

    return r


class AbstractTestSearch(object):
    """Class grouping common test code for search classes.

    Subclasses should implement at least the following public attributes
    in order for the tests defined here to be executed.

    Attributes
    ----------
    search_instance : pydov.search.abstract.AbstractSearch
        Instance of subclass of this type used for searching.
    datatype_class : pydov.types.abstract.AbstractDovType
            Class reference for the corresponding datatype.
    valid_query_single : owslib.fes2.OgcExpression
        OGC expression of a valid query returning a single result.
    inexistent_field : str
            The name of an inexistent field.
    wfs_field : str
        The name of a WFS field.
    xml_field : str
        The name of an XML field.
    valid_returnfields : tuple of str
        A tuple of valid return fields from the main type.
    valid_returnfields_subtype : typle of str
            A tuple containing valid return fields, including fields from a
            subtype.
    valid_returnfields_extra : tuple of str
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.
    df_default_columns : list of str
            A list of the column names of the default dataframe.

    """

    def test_pluggable_type(self):
        """Test whether the search object can be initialised by explicitly
        giving the objecttype.
        """
        datatype = self.datatype_class
        self.search_instance.__class__(objecttype=datatype)

    def test_get_fields(self, mp_wfs, mp_get_schema,
                        mp_remote_describefeaturetype, mp_remote_md,
                        mp_remote_fc, mp_remote_xsd):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.

        """
        fields = self.search_instance.get_fields()

        assert isinstance(fields, dict)

        for field in fields:
            assert isinstance(field, str)

            f = fields[field]
            assert isinstance(f, dict)

            assert 'name' in f
            assert isinstance(f['name'], str)
            assert f['name'] == field

            assert 'definition' in f
            assert isinstance(f['name'], str)

            assert 'type' in f
            assert isinstance(f['type'], str)
            assert f['type'] in ['string', 'float', 'integer', 'date',
                                 'datetime', 'boolean', 'geometry']

            assert 'list' in f
            assert isinstance(f['list'], bool)

            assert 'notnull' in f
            assert isinstance(f['notnull'], bool)

            assert 'query' in f
            assert isinstance(f['query'], bool)

            assert 'cost' in f
            assert isinstance(f['cost'], int)
            assert f['cost'] > 0

            if 'values' in f:
                assert sorted(f.keys()) == [
                    'cost', 'definition', 'list', 'name', 'notnull', 'query', 'type',
                    'values']

                assert isinstance(f['values'], dict)

                for v in f['values'].keys():
                    assert isinstance(f['values'][v], str) or f[
                        'values'][v] is None

                    if f['type'] == 'string':
                        assert isinstance(v, str)
                    elif f['type'] == 'float':
                        assert isinstance(v, float)
                    elif f['type'] == 'integer':
                        assert isinstance(v, int)
                    elif f['type'] == 'date':
                        assert isinstance(v, datetime.date)
                    elif f['type'] == 'datetime':
                        assert isinstance(v, datetime.datetime)
                    elif f['type'] == 'boolean':
                        assert isinstance(v, bool)
            else:
                assert sorted(f.keys()) == [
                    'cost', 'definition', 'list', 'name', 'notnull',
                    'query', 'type']

    def test_search_both_location_query(self, mp_get_schema,
                                        mp_remote_describefeaturetype,
                                        mp_remote_wfs_feature):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.search_instance.search(
            location=Within(Box(1, 2, 3, 4)),
            query=self.valid_query_single,
            return_fields=self.valid_returnfields)

        assert isinstance(df, DataFrame)

    def test_search(self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
                    mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                    mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
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
        df = self.search_instance.search(
            query=self.valid_query_single)

        assert isinstance(df, DataFrame)

        assert list(df) == self.df_default_columns

        datatype = self.datatype_class
        allfields = datatype.get_field_names()
        ownfields = datatype.get_field_names(include_subtypes=False)
        subfields = [f for f in allfields if f not in ownfields]

        assert len(df) >= 1

        # dtype checks of the resulting df columns
        fields = self.search_instance.get_fields()

        for field in list(df):
            if fields[field]['list']:
                # don't check uniqueness of list type values
                continue

            if field in ownfields:
                assert len(df[field].unique()) == 1
            elif field in subfields:
                assert len(df[field].unique()) >= 1

        for field in list(df):
            mandatory = fields[field]['notnull']
            if mandatory:
                assert len(df[field]) == len(df[field].dropna())

        for field in list(df):
            field_datatype = fields[field]['type']
            field_listtype = fields[field]['list']

            if field_listtype:
                datatypes = set(
                    (type(i) for i in
                     AbstractJoin._get_unique_value_list(df, field)))
            else:
                datatypes = set((type(i) for i in df[field].dropna()))

            assert len(datatypes) <= 1

            if len(datatypes) > 0:
                if field_datatype == 'string':
                    assert (str in datatypes)
                elif field_datatype == 'float':
                    assert float in datatypes
                elif field_datatype == 'integer':
                    assert (int in datatypes)
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
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=self.valid_returnfields)

        assert isinstance(df, DataFrame)

        assert list(df) == list(self.valid_returnfields.get_names())

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
        if self.valid_returnfields_subtype is None:
            return

        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=self.valid_returnfields_subtype)

        assert isinstance(df, DataFrame)

        assert list(df) == list(self.valid_returnfields_subtype.get_names())

    def test_search_returnfields_order(self, mp_remote_wfs_feature):
        """Test the search method with the query parameter and a selection of
        return fields in another ordering.

        Test whether the output dataframe contains only the selected return
        fields, in the order that is given in the return_fields parameter.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        rf = list(self.valid_returnfields.get_names())

        while rf == list(self.valid_returnfields):
            random.shuffle(rf)

        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=rf)

        assert isinstance(df, DataFrame)
        assert list(df) == rf

    def test_search_wrongreturnfields(self):
        """Test the search method with the query parameter and an inexistent
        return field.

        Test whether an InvalidFieldError is raised.

        """
        return_fields = list(self.valid_returnfields)
        return_fields.append(self.inexistent_field)

        with pytest.raises(InvalidFieldError):
            self.search_instance.search(
                query=self.valid_query_single,
                return_fields=return_fields)

    def test_search_wrongreturnfieldstype(self):
        """Test the search method with the query parameter and a single
        return field as string.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            self.search_instance.search(
                query=self.valid_query_single,
                return_fields=self.valid_returnfields[0])

    def test_search_query_wrongfield(self):
        """Test the search method with the query parameter using an
        inexistent query field.

        Test whether an InvalidFieldError is raised.

        """
        query = PropertyIsEqualTo(propertyname=self.inexistent_field,
                                  literal='The cat is out of the bag.')

        with pytest.raises(InvalidFieldError):
            self.search_instance.search(
                query=query)

    def test_search_query_wrongfield_returnfield(self):
        """Test the search method with the query parameter using an
        return-only field as query field.

        Test whether an InvalidFieldError is raised.

        """
        if self.xml_field is None:
            return

        query = PropertyIsEqualTo(propertyname=self.xml_field,
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            self.search_instance.search(query=query)

    def test_search_extrareturnfields(self, mp_get_schema,
                                      mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with the query parameter and an extra WFS
        field as return field.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        if self.valid_returnfields_extra is None:
            return

        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=self.valid_returnfields_extra)

        assert isinstance(df, DataFrame)

        assert list(df) == list(self.valid_returnfields_extra.get_names())

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_search_sortby_valid(self):
        """Test the search method with the query parameter and the sort_by
        parameter with a valid sort field.

        Test whether a dataframe is returned.
        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            sort_by=SortBy([SortProperty(
                self.valid_returnfields.get_names()[-1])]))

        assert isinstance(df, DataFrame)

    def test_search_sortby_invalid(self, mp_get_schema,
                                   mp_remote_describefeaturetype,
                                   mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with the query parameter and the sort_by
        parameter with an invalid sort field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        if self.xml_field is None:
            return

        with pytest.raises(InvalidFieldError):
            self.search_instance.search(
                query=self.valid_query_single,
                sort_by=SortBy([SortProperty(
                    self.xml_field)]))

    def test_search_xml_noresolve(self, mp_get_schema,
                                  mp_remote_describefeaturetype,
                                  mp_remote_wfs_feature, mp_dov_xml_broken):
        """Test the search method with return fields from WFS only.

        Test whether no XML is resolved.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml_broken : pytest.fixture
            Monkeypatch the call to break fetching of remote XML data.

        """
        self.search_instance.search(
            query=self.valid_query_single,
            return_fields=self.valid_returnfields_extra)

    def test_search_propertyinlist(self, mp_get_schema,
                                   mp_remote_describefeaturetype,
                                   mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with a PropertyInList query.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        self.search_instance.search(
            query=PropertyInList(self.wfs_field, ['a', 'b']))

    def test_search_join(self, mp_get_schema, mp_remote_describefeaturetype,
                         mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with a Join query.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df1 = self.search_instance.search(
            query=self.valid_query_single)

        self.search_instance.search(
            query=Join(df1, self.df_default_columns[0]))

    def test_get_fields_xsd_values(self, mp_remote_xsd):
        """Test the result of get_fields when the XML field has an XSD type.

        Test whether the output from get_fields() returns the values from
        the XSD.

        Parameters
        ----------
        mp_remote_xsd : pytest.fixture
            Monkeypatch the call to get XSD schemas.

        """
        xsd_schemas = self.datatype_class.get_xsd_schemas()

        if len(xsd_schemas) > 0:
            xml_fields = self.datatype_class.get_fields(source='xml')
            fields = self.search_instance.get_fields()
            for f in xml_fields.values():
                if 'xsd_type' in f:
                    assert 'values' in fields[f['name']]
                    assert isinstance(fields[f['name']]['values'], dict)

    def test_get_fields_no_xsd(self):
        """Test whether no XML fields have an XSD type when no XSD schemas
        are available."""
        xsd_schemas = self.datatype_class.get_xsd_schemas()

        if len(xsd_schemas) == 0:
            xml_fields = self.datatype_class.get_fields(source='xml')
            for f in xml_fields.values():
                assert 'xsd_type' not in f

    def test_get_fields_xsd_enums(self):
        """Test whether at least one XML field has an XSD type when there
        are XSD schemas available.

        Make sure XSD schemas are only listed (and downloaded) when they are
        needed.

        """
        xsd_schemas = self.datatype_class.get_xsd_schemas()

        xsd_type_count = 0

        if len(xsd_schemas) > 0:
            xml_fields = self.datatype_class.get_fields(source='xml')
            for f in xml_fields.values():
                if 'xsd_type' in f:
                    xsd_type_count += 1
            assert xsd_type_count > 0


class AbstractTestTypes(object):
    """Class grouping common test code for datatype classes.

    Subclasses should implement at least the following public attributes
    in order for the tests defined here to be executed.

    Attributes
    ----------
    datatype_class : pydov.types.abstract.AbstractDovType
        Class reference for the corresponding datatype.
    namespace : str
        WFS namespace for this type.
    pkey_base : str
        Base URL for the permanent keys of this datatype.
    field_names : list of str
        The field names for this type as listed in the documentation in
        docs/description_output_dataframes.rst
    field_names_subtypes : list of str
        The field names of this type that originate from subtypes only.
    field_names_nosubtypes : list of str
        The field names for this type, without including fields from
        subtypes.
    valid_returnfields : tuple of str
        A tuple of valid return fields from the main type.
    valid_returnfields_subtype : typle of str
            A tuple containing valid return fields, including fields from a
            subtype.
    inexistent_field : str
            The name of an inexistent field.

    """

    def test_get_field_names(self):
        """Test the get_field_names method.

        Tests whether the available fields for the type match the
        ones we list in docs/description_output_dataframes.rst.

        """
        fields = self.datatype_class.get_field_names()
        assert fields == self.field_names

    def test_get_field_names_nosubtypes(self):
        """Test the get_field_names method without including subtypes.

        Tests whether the fields provided in a subtype are not listed when
        disabling subtypes.

        """
        fields = self.datatype_class.get_field_names(
            return_fields=None, include_subtypes=False)

        assert fields == self.field_names_nosubtypes

    def test_get_field_names_returnfields_nosubtypes(self):
        """Test the get_field_names method when specifying return
        fields.

        Tests whether the returned fields match the ones provided as return
        fields.

        """
        fields = self.datatype_class.get_field_names(
            return_fields=self.valid_returnfields,
            include_subtypes=False)

        assert fields == list(self.valid_returnfields.get_names())

    def test_get_field_names_returnfields_order(self):
        """Test the get_field_names method when specifying return
        fields in a different order.

        Tests whether the returned fields match the ones provided as return
        fields and that the order is the one given in the return_fields
        parameter.

        """
        rf = ReturnFieldList(self.valid_returnfields)

        while rf == self.valid_returnfields:
            random.shuffle(rf)

        fields = self.datatype_class.get_field_names(
            return_fields=rf,
            include_subtypes=False)

        assert fields == rf.get_names()

    def test_get_field_names_wrongreturnfields(self):
        """Test the get_field_names method when specifying an
        inexistent return field.

        Test whether an InvalidFieldError is raised.

        """
        return_fields = self.valid_returnfields
        return_fields.append(ReturnField(self.inexistent_field))

        with pytest.raises(InvalidFieldError):
            self.datatype_class.get_field_names(
                return_fields=return_fields,
                include_subtypes=False)

    def test_get_field_names_wrongreturnfieldstype(self):
        """Test the get_field_names method when listing a single
        return field instead of a list.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            self.datatype_class.get_field_names(
                return_fields=self.valid_returnfields.get_names()[0],
                include_subtypes=False)

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        """
        if self.valid_returnfields_subtype is None:
            return

        with pytest.raises(InvalidFieldError):
            self.datatype_class.get_field_names(
                return_fields=self.valid_returnfields_subtype,
                include_subtypes=False)

    def test_get_fields(self):
        """Test the get_fields method.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        """
        fields = self.datatype_class.get_fields()

        assert isinstance(fields, OrderedDict)

        for f in fields.keys():
            assert isinstance(f, str)

            field = fields[f]
            assert isinstance(field, AbstractField)

            assert 'name' in field
            assert isinstance(field['name'], str)
            assert field['name'] == f

            assert 'source' in field
            assert isinstance(field['source'], str)
            assert field['source'] in ('wfs', 'xml')

            assert 'sourcefield' in field
            assert isinstance(field['sourcefield'], str)

            assert 'type' in field
            assert isinstance(field['type'], str)
            assert field['type'] in ['string', 'float', 'integer', 'date',
                                     'datetime', 'boolean', 'geometry']

            if field['source'] == 'wfs':
                if 'wfs_injected' in field.keys():
                    assert sorted(field.keys()) == [
                        'name', 'source', 'sourcefield', 'split_fn', 'type',
                        'wfs_injected']
                else:
                    assert sorted(field.keys()) == [
                        'name', 'source', 'sourcefield', 'split_fn', 'type']
            elif field['source'] == 'xml':
                assert 'definition' in field
                assert isinstance(field['definition'], str)

                assert 'notnull' in field
                assert isinstance(field['notnull'], bool)

                if 'xsd_type' in field:
                    assert sorted(field.keys()) == [
                        'definition', 'name', 'notnull', 'source',
                        'sourcefield', 'split_fn', 'type', 'xsd_schema',
                        'xsd_type']
                else:
                    assert sorted(field.keys()) == [
                        'definition', 'name', 'notnull', 'source',
                        'sourcefield', 'split_fn', 'type']

    def test_get_fields_nosubtypes(self):
        """Test the get_fields method not including subtypes.

        Test whether fields provides by subtypes are not listed in the output.

        """
        if self.field_names_subtypes is None:
            return

        fields = self.datatype_class.get_fields(include_subtypes=False)
        for field in fields:
            assert field not in self.field_names_subtypes

    def test_from_wfs_element(self, wfs_feature):
        """Test the from_wfs_element method.

        Test whether we can construct an instance from a WFS response element.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        feature = self.datatype_class.from_wfs_element(
            wfs_feature, self.namespace)

        assert isinstance(feature, self.datatype_class)

        if self.pkey_base is not None:
            assert feature.pkey.startswith(self.pkey_base)

            assert feature.pkey.startswith(
                build_dov_url('data/{}/'.format(feature.typename)))

        assert isinstance(feature.data, dict)
        assert isinstance(feature.subdata, dict)

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
        feature = self.datatype_class.from_wfs_element(
            wfs_feature, self.namespace)

        fields = [f for f in self.datatype_class.get_fields(
            source=('wfs', 'xml', 'custom_wfs', 'custom_xml')).values() if not
            f.get('wfs_injected', False)]

        df_array = feature.get_df_array()

        assert isinstance(df_array, list)

        def _test_data_type(field, value):
            if field['type'] == 'string':
                assert isinstance(value, str) or np.isnan(value)
            elif field['type'] == 'float':
                assert isinstance(value, float) or np.isnan(value)
            elif field['type'] == 'integer':
                assert isinstance(value, int) or np.isnan(value)
            elif field['type'] == 'date':
                assert isinstance(value, datetime.date) or np.isnan(value)
            elif field['type'] == 'boolean':
                assert isinstance(value, bool) or np.isnan(value)

            if field['name'].startswith('pkey') and not pd.isnull(value):
                assert value.startswith(build_dov_url('data/'))
                assert not value.endswith('.xml')

        for record in df_array:
            assert len(record) == len(fields)

            for value, field in zip(record, fields):
                if field['split_fn'] is not None:
                    assert isinstance(value, list)
                    for v in value:
                        _test_data_type(field, v)
                else:
                    _test_data_type(field, value)

    def test_get_df_array_wrongreturnfields(self, wfs_feature):
        """Test the get_df_array specifying a nonexistent return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        feature = self.datatype_class.from_wfs_element(
            wfs_feature, self.namespace)

        with pytest.raises(InvalidFieldError):
            feature.get_df_array(
                return_fields=ReturnFieldList.from_field_names(self.inexistent_field))

    def test_from_wfs_str(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as str.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returning str
            Fixture providing a WFS GetFeature response.

        """
        features = self.datatype_class.from_wfs(wfs_getfeature,
                                                self.namespace)

        for feature in features:
            assert isinstance(feature, self.datatype_class)

    def test_from_wfs_bytes(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as bytes.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returning str
            Fixture providing a WFS GetFeature response.

        """
        features = self.datatype_class.from_wfs(wfs_getfeature.encode('utf-8'),
                                                self.namespace)

        for feature in features:
            assert isinstance(feature, self.datatype_class)

    def test_from_wfs_tree(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as elementtree.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returning str
            Fixture providing a WFS GetFeature response.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        features = self.datatype_class.from_wfs(tree, self.namespace)

        for feature in features:
            assert isinstance(feature, self.datatype_class)

    def test_from_wfs_list(self, wfs_getfeature):
        """Test the from_wfs method to construct objects from a WFS response,
        as list of elements.

        Parameters
        ----------
        wfs_getfeature : pytest.fixture returning str
            Fixture providing a WFS GetFeature response.

        """
        tree = etree.fromstring(wfs_getfeature.encode('utf8'))
        feature_members = tree.find(
            './/{http://www.opengis.net/wfs/2.0}member')

        if feature_members is not None:
            fts = [ft for ft in feature_members]

            features = self.datatype_class.from_wfs(fts, self.namespace)

            for feature in features:
                assert isinstance(feature, self.datatype_class)

    def test_missing_pkey(self):
        """Test initialising an object type with a pkey of 'None'.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            self.datatype_class(None)

    def test_nested_subtype_from_xml_element(self, dov_xml):
        """Test initialising the subtype(s) from the XML document.

        Parameters
        ----------
        dov_xml : pytest.fixture returning bytes
            Fixture providing DOV XML data.
        """
        def instance_from_xml(clz, xml):
            if len(clz.subtypes) == 0:
                return

            if xml is None:
                return

            st_instance = next(
                clz.subtypes[0].from_xml(dov_xml))
            assert isinstance(st_instance, clz.subtypes[0])

            instance_from_xml(clz.subtypes[0], dov_xml)

        instance_from_xml(self.datatype_class, dov_xml)
