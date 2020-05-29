# -*- coding: utf-8 -*-
"""Module containing extra query classes to build attribute search queries."""

from owslib.fes import (
    Or,
    PropertyIsEqualTo,
    OgcExpression,
)


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


class Join(PropertyInList):
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

        value_list = list(dataframe[using].dropna().unique())

        if len(set(value_list)) < 1:
            raise ValueError("dataframe should contain at least a single "
                             "value in column '{}'.".format(using))

        super(Join, self).__init__(on, value_list)
