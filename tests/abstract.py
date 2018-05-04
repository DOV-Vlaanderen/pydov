import datetime

from numpy.compat import unicode


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
        """Test the resulting column dtypes from data.frame.

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
                assert df[field].dtype.name == 'object'
            elif datatype == 'float':
                assert df[field].dtype.name == 'float64'
            elif datatype == 'integer':
                assert df[field].dtype.name == 'integer'
            elif datatype == 'date':
                assert df[field].dtype.name == 'object'
            elif datatype == 'boolean':
                assert df[field].dtype.name == 'bool'
