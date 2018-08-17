import datetime
import numpy as np
from collections import OrderedDict

import pandas as pd
import requests
from numpy.compat import unicode
from pandas.api.types import (
    is_int64_dtype, is_object_dtype,
    is_bool_dtype, is_float_dtype)


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


class AbstractTestSearch(object):
    """Class grouping common test code for search classes."""
    @staticmethod
    def abstract_test_get_fields(fields):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

        Parameters
        ----------
        fields : dict
            Fields returned by a specific search class to test.

        """
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
                                 'boolean']

            assert 'notnull' in f
            assert type(f['notnull']) is bool

            assert 'cost' in f
            assert type(f['cost']) is int
            assert f['cost'] > 0

            if 'values' in f:
                assert sorted(f.keys()) == [
                    'cost', 'definition', 'name', 'notnull', 'type', 'values']
                for v in f['values']:
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
                                            'notnull', 'type']

    @staticmethod
    def abstract_test_df_dtypes(df, fields):
        """Test the resulting column dtypes from dataframe.

        Test whether the returned columns match the format specified
        in the documentation.

        Parameters
        ----------
        df : pd.DataFrame
            result of the search
        fields : dict
            Fields returned by a specific search class to test.

        """
        for field in list(df):
            datatype = fields[field]['type']
            if datatype == 'string':
                assert (is_object_dtype(df[field]) or
                        df[field].isnull().values.all())  # all Nan/None
            elif datatype == 'float':
                assert is_float_dtype(df[field])
            elif datatype == 'integer':
                assert is_int64_dtype(df[field])
            elif datatype == 'date':
                assert is_object_dtype(df[field])
            elif datatype == 'boolean':
                assert is_bool_dtype(df[field])

    @staticmethod
    def abstract_test_search_checkrows(df, datatype):
        """Test the number of rows in the result dataframe.

        Tests whether fields of the main datatype have only one value
        whereas the fields of a subtype may have multiple different values.

        Parameters
        ----------
        df : pd.DataFrame
            result of a search that returned a dataframe for a single
            instance of the datatype
        datatype : pydov.types.abstract.AbstractDovType
            datatype of the data in the resulting dataframe

        """
        allfields = datatype.get_field_names()
        ownfields = datatype.get_field_names(include_subtypes=False)
        subfields = [f for f in allfields if f not in ownfields]

        assert len(df) >= 1

        for field in list(df):
            if field in ownfields:
                assert len(df[field].unique()) == 1
            elif field in subfields:
                assert len(df[field].unique()) >= 1


class AbstractTestTypes(object):
    """Class grouping common test code for datatype classes."""
    @staticmethod
    def abstract_test_get_fields(fields):
        """Test the get_fields method of an AbstractDovType.

        Test whether the format returned by the method meets the
        requirements and the format listed in the docs.

        Parameters
        ----------
        fields : dict
            Fields returned by a specific datatype to test.

        """
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

                assert sorted(field.keys()) == [
                    'definition', 'name', 'notnull', 'source', 'sourcefield',
                    'type']

    @staticmethod
    def abstract_test_get_df_array(df_array, fields):
        """Test the output of the get_df_array method.

        Test whether the output of the dataframe array is correct.

        Parameters
        ----------
        df_array : list
            Dataframe array to test.
        fields : list
            Fields to test against.

        """
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
