# -*- coding: utf-8 -*-
"""Module containing generic custom fields."""

import numpy as np

from pydov.types.fields import _CustomXmlField
from pydov.util.codelists import OsloCodeList


class MvMtawField(_CustomXmlField):
    """Field for retrieving the mv_mtaw value from the height of the point in
    relevant cases."""

    def __init__(self, definition):
        """Initialise a MvMtawField (mv_mtaw) with given definition.

        Parameters
        ----------
        definition : string
            Type-specific definition of the mv_mtaw field.
        """
        super().__init__(
            name='mv_mtaw',
            definition=definition,
            datatype='float',
            notnull=False
        )

    def calculate(self, cls, tree):
        # Support the old format too
        oorspronkelijk_maaiveld = cls._parse(
            func=tree.findtext,
            xpath='.//oorspronkelijk_maaiveld/waarde',
            namespace=None,
            returntype='float'
        )
        if oorspronkelijk_maaiveld is not np.nan:
            return oorspronkelijk_maaiveld

        # Check if referentiepunt is Maaiveld
        referentiepunt = cls._parse(
            func=tree.findtext,
            xpath='.//ligging/metadata_hoogtebepaling/referentiepunt_type',
            namespace=None,
            returntype='string'
        )
        if referentiepunt != 'Maaiveld':
            # If referentiepunt is not Maaiveld, we don't know the height of
            # maaiveld
            return np.nan

        # If referentiepunt is Maaiveld, height of the ligging is Maaiveld
        point = tree.findtext(
            './/ligging/{http://www.opengis.net/gml/3.2}Point/'
            '{http://www.opengis.net/gml/3.2}pos'
        )
        coords = point.split(' ')
        if len(coords) == 3:
            hoogte = float(coords[-1])
            return hoogte
        else:
            return np.nan


class OsloCodeListValueField(_CustomXmlField):
    def __init__(self, name, source_xpath, datatype, definition, conceptscheme,
                 notnull=False):
        """Initialise an OsloCodeListValueField.

        This field will return the code part of an OSLO codelist value URI,
        and associate it with an OsloCodeList based on the given
        conceptscheme.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source_xpath : str
            XPath expression of the values of this field in the source XML
            document.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.
        definition : str
            Definition of this field.
        conceptscheme : str
            OSLO conceptscheme which will be used for the associated codelist.
        notnull : bool, optional, defaults to False
            True if this field is always present (mandatory), False otherwise.
        """
        super().__init__(name, datatype, definition, notnull)
        self.source_xpath = source_xpath
        self.conceptscheme = conceptscheme

        self.__setitem__('codelist', OsloCodeList(
            self.conceptscheme, datatype
        ))

    def calculate(self, cls, tree):
        value_uri = cls._parse(
            func=tree.findtext,
            xpath=self.source_xpath,
            namespace=None,
            returntype=self.get('type')
        )
        if value_uri is np.nan or value_uri == '':
            return np.nan

        code = value_uri.split('/')[-1]
        return cls._typeconvert(code, self.get('type'))
