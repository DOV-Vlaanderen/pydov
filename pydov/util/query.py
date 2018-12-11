# -*- coding: utf-8 -*-
"""Module containing extra query classes to build attribute search queries."""

from owslib.fes import (
    Or,
    PropertyIsEqualTo,
)


class PropertyInList(Or):
    def __init__(self, propertyname, list):
        if len(set(list)) < 2:
            raise ValueError('list should contain at least two different '
                             'elements.')

        super(PropertyInList, self).__init__(
            [PropertyIsEqualTo(propertyname, i) for i in set(list)]
        )


class Join(PropertyInList):
    def __init__(self, dataframe, join_column):
        if join_column not in list(dataframe):
            raise ValueError('join_column should be present in the dataframe.')

        value_list = list(dataframe[join_column].dropna().unique())

        if len(set(value_list)) < 2:
            raise ValueError("dataframe should contain at least two "
                             "different values in column '%s'." % join_column)

        super(Join, self).__init__(join_column, value_list)
