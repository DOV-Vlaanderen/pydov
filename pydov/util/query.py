# -*- coding: utf-8 -*-
"""Module containing extra query classes to build attribute search queries."""

from owslib.fes import (
    Or,
    PropertyIsEqualTo,
)


class PropertyInList(Or):
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
            If the given list does not contain at least two distinct items.

        """
        if not isinstance(lst, list) and not isinstance(lst, set):
            raise ValueError('list should be of type "list" or "set"')

        if len(set(lst)) < 2:
            raise ValueError('list should contain at least two different '
                             'elements.')

        super(PropertyInList, self).__init__(
            [PropertyIsEqualTo(propertyname, i) for i in set(lst)]
        )


class Join(PropertyInList):
    """Filter expression to join different searches together.

    Internally translates to a PropertyInList:

    Join(df, 'pkey_boring') is equivalent to

    PropertyInList('pkey_boring', list(df['pkey_boring')) which is
    equivalent to

    Or([PropertyIsEqualTo('pkey_boring', x), PropertyIsEqualTo(
    'pkey_boring', y), ...]) for every x, y, in df['pkey_boring']

    """
    def __init__(self, dataframe, join_column):
        """Initialisation.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Dataframe to use a basis for joining.
        join_column : str
            Name of the column to join on. This column should both exists in
            the dataframe and in the object type being searched.

        Raises
        ------
        ValueError
            If the join_column is not present in the dataframe.

            If the dataframe does not contain at least two different values
            in the join_column. A Join is probably overkill here,
            use PropertyIsEqualTo instead.

        """
        if join_column not in list(dataframe):
            raise ValueError('join_column should be present in the dataframe.')

        value_list = list(dataframe[join_column].dropna().unique())

        if len(set(value_list)) < 2:
            raise ValueError("dataframe should contain at least two "
                             "different values in column '%s'." % join_column)

        super(Join, self).__init__(join_column, value_list)
