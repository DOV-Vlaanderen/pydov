# -*- coding: utf-8 -*-
"""Module containing extra query classes to build attribute search queries."""

from owslib.fes2 import OgcExpression, Or, PropertyIsEqualTo, PropertyIsLike


class PropertyInList(OgcExpression):
    """Filter expression to test whether a given property has one of the
    values from a list.

    Internally translates to an Or combination of PropertyIsEqualTo
    expressions:

    PropertyInList('methode', ['spade', 'spoelboring']) is equivalent to

    Or([PropertyIsEqualTo('methode', 'spade'), PropertyIsEqualTo('methode',
    'spoelboring')])

    """

    def __init__(self, propertyname, lst):
        """Initialisation.

        Parameters
        ----------
        propertyname : str
            Name of the attribute to query.
        lst : list of str
            List of literals to match against (exact matches).

        Raises
        ------
        ValueError
            If the given list does not contain at least a single item.

        """
        super(PropertyInList, self).__init__()

        if not isinstance(lst, list) and not isinstance(lst, set):
            raise ValueError('list should be of type "list" or "set"')

        if len(set(lst)) < 1:
            raise ValueError('list should contain at least a single item')
        elif len(set(lst)) == 1:
            self.query = PropertyIsEqualTo(propertyname, set(lst).pop())
        else:
            self.query = Or(
                [PropertyIsEqualTo(propertyname, i) for i in sorted(set(lst))])

    def toXML(self):
        """Return the XML representation of the PropertyInList query.

        Returns
        -------
        xml : etree.ElementTree
            XML representation of the PropertyInList

        """
        return self.query.toXML()


class PropertyLikeList(OgcExpression):
    """Filter expression to test whether a given property is like one of the
    values from a list.

    Internally translates to an Or combination of PropertyIsLike
    expressions:

    PropertyLikeList('methode', ['spade', 'spoelboring'], '%{item}%') is
    equivalent to

    Or([PropertyIsLike('methode', '%spade%'), PropertyIsLike('methode',
    '%spoelboring%')])

    """

    def __init__(self, propertyname, lst, modifier='%{item}%'):
        """Initialisation.

        Parameters
        ----------
        propertyname : str
            Name of the attribute to query.
        lst : list of str
            List of item literals to match against.
        modifier : str
            Optional, modifier to apply to the lst items when constructing the
            query. You can use the string '{item}' in it which will be replaced
            by the lst item.

        Raises
        ------
        ValueError
            If the given list does not contain at least a single item.
            If the modifier is not of type str.

        """
        super(PropertyLikeList, self).__init__()

        if not isinstance(lst, list) and not isinstance(lst, set):
            raise ValueError('list should be of type "list" or "set"')

        if not isinstance(modifier, str):
            raise ValueError('modifier should be of type "str"')

        if len(set(lst)) < 1:
            raise ValueError('list should contain at least a single item')
        elif len(set(lst)) == 1:
            self.query = PropertyIsLike(
                propertyname, modifier.format(item=set(lst).pop()))
        else:
            self.query = Or(
                [PropertyIsLike(propertyname, modifier.format(item=i)) for i
                 in sorted(set(lst))])

    def toXML(self):
        """Return the XML representation of the PropertyInList query.

        Returns
        -------
        xml : etree.ElementTree
            XML representation of the PropertyInList

        """
        return self.query.toXML()


class AbstractJoin:
    """Abstract base class for the Join classes."""

    @staticmethod
    def _is_iterable_type(dataframe, column):
        """Check if the first element in a specified column of a dataframe is
        an iterable type (list or set).

        Parameters
        ----------
        dataframe : pandas.DataFrame
            A pandas DataFrame containing the data.
        column : str
            The name of the column to check.

        Returns
        -------
        bool
            True if the first element of the column is a list or set, False
            otherwise.

        Raises
        ------
        ValueError
            If the input dataframe is empty.

        """
        if len(dataframe) < 1:
            raise ValueError("dataframe should not be empty")

        return isinstance(dataframe[column].iloc[0], list) or \
            isinstance(dataframe[column].iloc[0], set)

    @staticmethod
    def _get_unique_value_list(dataframe, column):
        """Retrieve a list of unique values from a specified column in a pandas
        DataFrame. If the values are iterable (list or set), it aggregates
        them.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            A pandas DataFrame containing the data.
        column : str
            The name of the column to process.

        Returns
        -------
        list
            A list of unique values from the specified column, possibly
            aggregating iterable values.

        Raises
        ------
        ValueError
            If the input dataframe is empty.

        """
        if AbstractJoin._is_iterable_type(dataframe, column):
            value_list = dataframe[column].dropna().aggregate('sum')
            return list(set(value_list))

        return list(dataframe[column].dropna().unique())


class Join(AbstractJoin, PropertyInList):
    """Filter expression to join different searches together.

    Internally translates to a PropertyInList:

    Join(df, 'pkey_boring') is equivalent to

    PropertyInList('pkey_boring', list(df['pkey_boring')) which is
    equivalent to

    Or([PropertyIsEqualTo('pkey_boring', x), PropertyIsEqualTo(
    'pkey_boring', y), ...]) for every x, y, in df['pkey_boring']

    """

    def __init__(self, dataframe, on, using=None):
        """Initialisation.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataframe to use a basis for joining.
        on : str
            Name of the column in the queried datatype to join on.
        using : str, optional
            Name of the column in the dataframe to use for joining. By
            default, the same column name as in `on` is assumed.

        Raises
        ------
        ValueError
            If the `using` column is not present in the dataframe.

            If `using` is None and the `on` column is not present in the
            dataframe.

            If the dataframe does not contain at least a single non-null value
            in the `using` column.

        """
        if using is None:
            using = on

        if using not in list(dataframe):
            raise ValueError(
                "column '{}' should be present in the dataframe.".format(
                    using))

        value_list = self._get_unique_value_list(dataframe, using)

        if len(set(value_list)) < 1:
            raise ValueError("dataframe should contain at least a single "
                             "value in column '{}'.".format(using))

        super(Join, self).__init__(on, value_list)


class FuzzyJoin(AbstractJoin, PropertyLikeList):
    """Filter expression to join different searches together in a fuzzy
    (non-exact) way.

    Internally translates to a PropertyLikeList:

    FuzzyJoin(df, 'pkey_boring', modifier='%|{item}|%') is equivalent to

    PropertyLikeList('pkey_boring', list(df['pkey_boring'),
                     modifier='%|{item}|%')
    which is equivalent to

    Or([PropertyIsLike('pkey_boring', '%|x|%'), PropertyIsLike(
    'pkey_boring', '%|y|%'), ...]) for every x, y, in df['pkey_boring']

    """

    def __init__(self, dataframe, on, using=None, modifier='%|{item}|%'):
        """Initialisation.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataframe to use a basis for joining.
        on : str
            Name of the column in the queried datatype to join on.
        using : str, optional
            Name of the column in the dataframe to use for joining. By
            default, the same column name as in `on` is assumed.
        modifier : str, optional, defaults to `'%|{item}|%'`
            Optional, modifier to apply to the dataframe items when
            constructing the query. You can use the string '{item}' in it which
            will be replaced by the dataframe item.

        Raises
        ------
        ValueError
            If the `using` column is not present in the dataframe.

            If `using` is None and the `on` column is not present in the
            dataframe.

            If the dataframe does not contain at least a single non-null value
            in the `using` column.

        """
        if using is None:
            using = on

        if using not in list(dataframe):
            raise ValueError(
                "column '{}' should be present in the dataframe.".format(
                    using))

        value_list = self._get_unique_value_list(dataframe, using)

        if len(set(value_list)) < 1:
            raise ValueError("dataframe should contain at least a single "
                             "value in column '{}'.".format(using))

        super(FuzzyJoin, self).__init__(on, value_list, modifier)
