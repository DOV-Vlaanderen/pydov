# -*- coding: utf-8 -*-
"""Module containing the base DOV data types."""

import datetime
import types
from collections import OrderedDict

from owslib.etree import etree
from owslib.util import openURL


class AbstractDovType(object):
    """Abstract DOV type grouping fields and methods common to all DOV
    object types. Not to be instantiated or used directly."""

    _UNRESOLVED = "{UNRESOLVED}"
    _fields = []

    def __init__(self, typename, pkey):
        """Initialisation.

        Parameters
        ----------
        typename : str
            Name of the DOV object type.
        pkey : str
            Permanent key of this DOV object, being a URI of the form
            `https://www.dov.vlaanderen.be/data/typename/id`.

        """
        self.typename = typename
        self.pkey = pkey

        self.data = dict(
            zip(self.get_field_names(),
                [AbstractDovType._UNRESOLVED] * len(self.get_field_names()))
        )

        self.data['pkey_%s' % self.typename] = self.pkey

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build an instance of this type from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    @classmethod
    def from_wfs(cls, response, namespace):
        """Build instances of this type from a WFS response.

        Parameters
        ----------
        response : str or bytes or iterable<etree.Element>
            WFS response containing GML features.

            Can either be a GML `str` or `byte` sequence, in which case it
            will be parsed and scanned for `gml:featureMembers`.

            It can also be an iterable (list, tuple or generator) of
            `etree.Element` in which case it will be looped over.
        namespace : str
             Namespace associated with this WFS featuretype.

        Yields
        ------
            An instance of this type for each record in the WFS response.

        """
        if type(response) is str:
            response = response.encode('utf8')

        if type(response) is bytes:
            tree = etree.fromstring(response)

            for ft in tree.find('.//{http://www.opengis.net/gml}'
                                'featureMembers'):
                yield (cls.from_wfs_element(ft, namespace))

        if type(response) in (list, tuple, set) \
                or isinstance(response, types.GeneratorType):
            for el in response:
                yield (cls.from_wfs_element(el, namespace))

    @classmethod
    def get_field_names(cls, return_fields=None):
        """Return the names of the fields available for this type.

        Returns
        -------
        list<str>
            List of the field names available for this type. These are also
            the names of the columns in the output dataframe for this type.
        return_fields : list<str> or tuple<str> or set<str> or iterable<str>
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.

        """
        if return_fields is None:
            return [f['name'] for f in cls._fields]
        else:
            return [f['name'] for f in cls._fields if f['name'] in
                    return_fields]

    @classmethod
    def get_fields(cls, source=('wfs', 'xml')):
        """Return the metadata of the fields available for this type.

        Parameters
        ----------
        source : list<str> or tuple<str> or iterable<str>
            A list of sources to include in the output. Can either be `wfs` or
            `xml` or `wfs, xml`.

        Returns
        -------
        collections.OrderedDict<str,dict>
            Ordered dictionary mapping the field (column) name to the
            dictionary containing the metadata of this field.

            This metadata dictionary includes at least:

            name (str)
                The name of the field in the output data.

            source (str)
                The source of the field (either `wfs` or `xml`).

            sourcefield (str)
                The name of the field in the source (source + sourcefield
                identify the origin of the data).

            type (str)
                Datatype of the output data field (one of `string`, `float`,
                `integer`, `date`, `datetime`).

            The metadata dictionary additionally includes for fields with
            source `xml`:

            definition (str)
                The definition of the field.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

        """
        return OrderedDict(
            zip([f['name'] for f in cls._fields if f['source'] in source],
                [f for f in cls._fields if f['source'] in source]))

    @classmethod
    def to_df_array(cls, iterable, return_fields=None):
        """Yield a dataframe array for each instance in the given iterable.

        Parameters
        ----------
        iterable : list<DovType> or tuple<DovType> or iterable<DovType>
            A list of instances of a DOV type.
        return_fields : list<str> or tuple<str> or set<str> or iterable<str>
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.

        Yields
        ------
        list
            List of the values of the instance in the same order as the
            field/column names, for inclusion in the result dataframe of a
            search operation.

        """
        for item in iterable:
            yield (item.get_df_array(return_fields))

    @classmethod
    def _parse(cls, func, xpath, namespace, returntype):
        """Parse the result of an XML path function, stripping the namespace
        and adding type conversion.

        Parameters
        ----------
        func : reference to function
           Function to call.
        xpath : str
            XML path of the element, used as the argument of `func`.
        namespace : str or None
            Namespace to be added to each item in the `xpath`. None to use
            the xpath as is.
        returntype : str
            Parse the text found with `func` to this output datatype. One of
            `string`, `float`, `integer`, `date`.

        Returns
        -------
        str or float or int or datetime.date
            Returns the parsed value of the output from calling `func` on
            `xpath`, converted to the type described by `returntype`.

        """
        def typeconvert(x):
            return x

        if returntype == 'string':
            def typeconvert(x):
                return str(x).strip()
        elif returntype == 'integer':
            def typeconvert(x):
                return int(x)
        elif returntype == 'float':
            def typeconvert(x):
                return float(x)
        elif returntype == 'date':
            def typeconvert(x):
                return datetime.datetime.strptime(x, '%Y-%m-%dZ').date()

        if namespace is not None:
            ns = '{%s}' % namespace
            text = func('./' + ns + ('/' + ns).join(xpath.split('/')))
        else:
            text = func('./' + xpath.lstrip('/'))

        if text is None:
            return None
        return typeconvert(text)

    def _get_xml_data(self):
        """Return the raw XML data for this DOV object.

        Returns
        -------
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        return openURL(self.pkey + '.xml').read()

    def _parse_xml_data(self):
        """Get remote XML data for this DOV object, parse the raw XML and
        save the results in the data object.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def get_df_array(self, return_fields=None):
        """Return the data array of the instance of this type for inclusion
        in the resulting output dataframe of a search operation.

        Parameters
        ----------
        return_fields : list<str> or tuple<str> or set<str> or iterable<str>
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.

        Returns
        -------
        list
            List of the values of this instance in the same order as the
            field/column names, for inclusion in the result dataframe of a
            search operation.

        """
        if return_fields is None:
            data = [self.data[c] for c in self.get_field_names()]
        else:
            data = [self.data[c] for c in self.get_field_names() if c in
                    return_fields]

        if self._UNRESOLVED in data:
            self._parse_xml_data()
            data = self.get_df_array(return_fields)

        return data


class Boring(AbstractDovType):
    """Class representing the DOV data type for boreholes."""

    _fields = [{
        'name': 'pkey_boring',
        'source': 'wfs',
        'sourcefield': 'fiche',
        'type': 'string'
    }, {
        'name': 'boornummer',
        'source': 'wfs',
        'sourcefield': 'boornummer',
        'type': 'string'
    }, {
        'name': 'x',
        'source': 'wfs',
        'sourcefield': 'X_mL72',
        'type': 'float'
    }, {
        'name': 'y',
        'source': 'wfs',
        'sourcefield': 'Y_mL72',
        'type': 'float'
    }, {
        'name': 'mv_mtaw',
        'source': 'xml',
        'sourcefield': '/boring/oorspronkelijk_maaiveld/waarde',
        'definition': 'Maaiveldhoogte in mTAW op dag dat de boring '
                      'uitgevoerd werd.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'start_boring_mtaw',
        'source': 'wfs',
        'sourcefield': 'Z_mTAW',
        'type': 'float'
    }, {
        'name': 'diepte_boring_van',
        'source': 'xml',
        'sourcefield': '/boring/diepte_van',
        'definition': 'Startdiepte van de boring (in meter).',
        'type': 'float',
        'notnull': True
    }, {
        'name': 'diepte_boring_tot',
        'source': 'wfs',
        'sourcefield': 'diepte_tot_m',
        'type': 'float'
    }, {
        'name': 'datum_aanvang',
        'source': 'wfs',
        'sourcefield': 'datum_aanvang',
        'type': 'date'
    }, {
        'name': 'uitvoerder',
        'source': 'wfs',
        'sourcefield': 'uitvoerder',
        'type': 'string'
    }, {
        'name': 'boorgatmeting',
        'source': 'xml',
        'sourcefield': '/boring/boorgatmeting/uitgevoerd',
        'definition': 'Is er een boorgatmeting uitgevoerd (ja/nee).',
        'type': 'boolean',
        'notnull': False
    }, {
        'name': 'diepte_methode_van',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/van',
        'definition': 'Bovenkant van de laag die met een bepaalde '
                      'methode aangeboord werd, in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'diepte_methode_tot',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/tot',
        'definition': 'Onderkant van de laag die met een bepaalde '
                      'methode aangeboord werd, in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'boormethode',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/methode',
        'definition': 'Boormethode voor het diepte-interval.',
        'type': 'string',
        'notnull': False
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Boring (borehole), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(Boring, self).__init__('boring', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `Boring` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        boring : Boring
            An instance of this class populated with the data from the WFS
            element.

        """
        b = Boring(feature.findtext('./{%s}fiche' % namespace))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return b

    def _parse_xml_data(self):
        """Get remote XML data for this DOV object, parse the raw XML and
        save the results in the data object.
        """
        data = self._get_xml_data()
        tree = etree.fromstring(data)

        for field in self.get_fields(source=('xml',)).values():
            self.data[field['name']] = self._parse(
                func=tree.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )
