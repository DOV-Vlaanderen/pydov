# -*- coding: utf-8 -*-
"""Module containing the base DOV data types."""

import types
import warnings
from collections import OrderedDict

import numpy as np
from owslib.etree import etree

import pydov
from pydov.search.abstract import AbstractCommon
from pydov.types.fields import AbstractField, ReturnFieldList
from pydov.util import owsutil
from pydov.util.dovutil import get_dov_xml, parse_dov_xml
from pydov.util.errors import RemoteFetchError, XmlFetchWarning
from pydov.util.net import LocalSessionThreadPool

from ..util.errors import InvalidFieldError, XmlParseError, XmlParseWarning
from ..util.hooks import HookRunner


class AbstractTypeCommon(AbstractCommon):
    """Class grouping methods common to AbstractDovType and
    AbstractDovSubType.

    Attributes
    ----------
    fields : list of pydov.types.fields.AbstractField
        List of fields of this type.

    """

    fields = []

    @classmethod
    def _parse(cls, func, xpath, namespace, returntype, split_fn=None):
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
            `string`, `float`, `integer`, `date`, `datetime`, `boolean`.
        split_fn : optional, function
            Function to split values from this field into a list of values.
            After splitting they will be parsed into the corresponding
            returntype.

        Returns
        -------
        str or float or int or bool or datetime.date or datetime.datetime
            Returns the parsed value of the output from calling `func` on
            `xpath`, converted to the type described by `returntype`.

        """
        if namespace is not None:
            ns = '{{{}}}'.format(namespace)
            text = func('./' + ns + ('/' + ns).join(xpath.split('/')))
        else:
            text = func('./' + xpath.lstrip('/'))

        if text is None:
            return np.nan

        if split_fn is not None:
            items = split_fn(text)
            return [cls._typeconvert(item, returntype) for item in items]

        return cls._typeconvert(text, returntype)

    @classmethod
    def extend_fields(cls, extra_fields):
        """Extend the fields of this type with given extra fields and return
        the new fieldset.

        Parameters
        ----------
        extra_fields : list of pydov.types.fields.AbstractField
            Extra fields to be appended to the existing fields of this type.

        Returns
        -------
        list of pydov.types.fields.AbstractField
            List of the existing fields of this type, extended with the
            extra fields supplied in extra_fields.

        """
        fields = list(cls.fields)
        fields.extend(extra_fields)
        return fields


class AbstractDovSubType(AbstractTypeCommon):
    """Abstract DOV type grouping fields and methods common to all DOV
    subtypes. Not to be instantiated or used directly.

    Attributes
    ----------
    rootpath : str
        XPath expression of the root element of this subtype. Should return
        all elements of this subtype.

    Raises
    ------
    RuntimeError
        When the defined fields of this type are invalid.

    """

    rootpath = None

    subtypes = []

    _UNRESOLVED = "{UNRESOLVED}"

    def __init__(self):
        """Initialisation.

        Parameters
        ----------
        name : str
            The name associated with this subtype.

        """
        for f in self.fields:
            if not isinstance(f, AbstractField):
                raise RuntimeError(
                    "Subtype '{}' fields should be instances of "
                    "pydov.types.fields.AbstractField, found {}.".format(
                        self.__class__.__name__, str(type(f))))

        self.data = dict(
            zip(self.get_field_names(),
                [AbstractDovSubType._UNRESOLVED] * len(self.get_field_names()))
        )

        self.subdata = dict(
            zip([st.get_name() for st in self.subtypes],
                [] * len(self.subtypes))
        )

    @classmethod
    def from_xml(cls, xml_data):
        """Build instances of this subtype from XML data.

        Parameters
        ----------
        xml_data : bytes
            Raw XML data of the DOV object that contains information about
            this subtype.

        Yields
        ------
            An instance of this type for each occurrence of the rootpath in
            the XML document.

        """
        try:
            tree = parse_dov_xml(xml_data)
            for element in tree.xpath(cls.rootpath):
                yield cls.from_xml_element(element)
        except XmlParseError:
            # Ignore XmlParseError here in subtypes, assuming it will be
            # reported in the corresponding main type. We can make this
            # assumption safely because both main and subtypes are in a
            # single XML file.
            pass

    @classmethod
    def from_xml_element(cls, element):
        """Build an instance of this subtype from a single XML element.

        Parameters
        ----------
        element : etree.Element
            XML element representing a single record of this subtype.

        Returns
        -------
        instance of this class
            An instance of this class based on the data in the XML element.

        """
        instance = cls()

        for field in cls.get_fields().values():
            instance.data[field['name']] = instance._parse(
                func=element.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None),
                split_fn=field.get('split_fn', None)
            )

        instance._parse_subtypes(etree.tostring(element))
        return instance

    @classmethod
    def get_field_names(cls):
        """Return the names of the fields available for this subtype.

        Returns
        -------
        list<str>
            List of the field names available for this type. These are also
            the names of the columns in the output dataframe for this type.

        """
        field_names = [f['name'] for f in cls.fields]

        for st in cls.subtypes:
            field_names.extend(st.get_field_names())

        return field_names

    @classmethod
    def get_fields(cls):
        """Return the metadata of the fields available for this subtype.

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

            definition (str)
                The definition of the field.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

        """
        fields = OrderedDict(
            zip([f['name'] for f in cls.fields],
                [f for f in cls.fields]))

        for st in cls.subtypes:
            fields.update(OrderedDict(
                zip([f['name'] for f in st.fields],
                    [f for f in st.fields])
            ))

        return fields

    @classmethod
    def get_name(cls):
        """Return the name associated with this subtype.

        Returns
        -------
        name : str
            The name associated with this subtype.

        """
        return cls.__name__

    def _parse_subtypes(self, xml):
        """Parse the subtypes with the given XML data.

        Parameters
        ----------
        xml : bytes
            The raw XML data of the DOV object as bytes.

        """
        for subtype in self.subtypes:
            st_name = subtype.get_name()
            if st_name not in self.subdata:
                self.subdata[st_name] = []

            for subitem in subtype.from_xml(xml):
                self.subdata[st_name].append(subitem)

    def get_data_dicts(self):
        """Return the data dictionaries for this instance, including subtypes,
        for inclusion in the output dataframe.

        Returns
        -------
        list(dict)
            list of data dictionaries for inclusion in the output dataframe
        """
        datadicts = []

        if len(self.subdata) == 0:
            datadicts.append(self.data)
        else:
            for subtype in self.subdata:
                if len(self.subdata[subtype]) == 0:
                    datadicts.append(self.data)
                else:
                    for subdata in self.subdata[subtype]:
                        for subdata_dict in subdata.get_data_dicts():
                            datadict = {}
                            datadict.update(self.data)
                            datadict.update(subdata_dict)
                            datadicts.append(datadict)

        return datadicts


class AbstractDovType(AbstractTypeCommon):
    """Abstract DOV type grouping fields and methods common to all DOV
    object types. Not to be instantiated or used directly.

    Attributes
    ----------
    subtypes : list of subclass of pydov.types.abstract.AbstractDovSubType
        List of subtypes of this type.

    """

    _UNRESOLVED = "{UNRESOLVED}"

    subtypes = []
    fields = []
    pkey_fieldname = None

    def __init__(self, typename, pkey):
        """Initialisation.

        Parameters
        ----------
        typename : str
            Name of the DOV object type.
        pkey : str
            Permanent key of this DOV object, being a URI of the form
            `https://www.dov.vlaanderen.be/data/typename/id`.

        Raises
        ------
        RuntimeError
            When the defined fields of this type are invalid.

        """
        if typename is None or pkey is None:
            raise ValueError(
                "Failed to instantiate object of class {} with typename '{}' "
                "and permkey '{}'. Typename and pkey must not be None.".format(
                    self.__class__.__name__, typename, pkey))

        self.typename = typename
        self.pkey = pkey

        for f in self.fields:
            if not isinstance(f, AbstractField):
                raise RuntimeError(
                    "Type '{}' fields should be instances of "
                    "pydov.types.fields.AbstractField, found {}.".format(
                        self.__class__.__name__, str(type(f))))

        self.data = dict(
            zip(self.get_field_names(include_subtypes=False),
                [AbstractDovType._UNRESOLVED] * len(self.get_field_names()))
        )

        self.subdata = dict(
            zip([st.get_name() for st in self.subtypes],
                [] * len(self.subtypes))
        )

        self.data['pkey_{}'.format(self.typename)] = self.pkey

    def _parse_xml_data(self, session=None):
        """Get remote XML data for this DOV object, parse the raw XML and
        save the results in the data object.

        Parameters
        ----------
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        success : boolean
            Whether or not the XML data could be fetched and parsed.

        """
        try:
            xml = self._get_xml_data(session)
        except RemoteFetchError:
            warnings.warn(("Failed to fetch remote XML document for "
                           "object '{}'. Resulting dataframe will be "
                           "incomplete.".format(self.pkey)), XmlFetchWarning)
            return False

        try:
            tree = parse_dov_xml(xml)

            for field in self.get_fields(source=('xml',),
                                         include_subtypes=False).values():
                self.data[field['name']] = self._parse(
                    func=tree.findtext,
                    xpath=field['sourcefield'],
                    namespace=None,
                    returntype=field.get('type', None),
                    split_fn=field.get('split_fn', None)
                )

            for field in self.get_fields(source=('custom_xml',),
                                         include_subtypes=False).values():
                self.data[field['name']] = field.calculate(
                    self.__class__, tree) or np.nan

            self._parse_subtypes(xml)
            return True
        except XmlParseError:
            warnings.warn(
                ("Failed to parse XML for object '{}'. Resulting "
                    "dataframe will be incomplete.").format(self.pkey),
                XmlParseWarning)
            return False

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build an instance of this type from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        cls
            An instance of this class populated with the data from the WFS
            element.

        """
        if cls.pkey_fieldname is not None:
            pkey = feature.findtext(
                './{{{}}}{}'.format(namespace, cls.pkey_fieldname))
        else:
            pkey = feature.get('{http://www.opengis.net/gml/3.2}id')

        instance = cls(pkey)

        for field in cls.get_fields(source=('wfs',)).values():
            if owsutil.has_geom_support() and field['type'] == 'geometry':
                instance.data[field['name']] = cls._parse(
                    func=feature.find,
                    xpath=field['sourcefield'],
                    namespace=namespace,
                    returntype='geometry'
                )
            else:
                instance.data[field['name']] = cls._parse(
                    func=feature.findtext,
                    xpath=field['sourcefield'],
                    namespace=namespace,
                    returntype=field.get('type', str),
                    split_fn=field.get('split_fn', None)
                )

        for field in cls.get_fields(source=('custom_wfs',)).values():
            for required_field in field.requires_wfs_fields():
                instance.data[required_field] = cls._parse(
                    func=feature.findtext,
                    xpath=required_field,
                    namespace=namespace,
                    returntype=field.get('type', str),
                    split_fn=field.get('split_fn', None)
                )

        for field in cls.get_fields(source=('custom_wfs',)).values():
            instance.data[field['name']] = field.calculate(instance) or np.nan

        return instance

    @classmethod
    def from_wfs(cls, response, namespace):
        """Build instances of this type from a WFS response.

        Parameters
        ----------
        response : str or bytes or etree.Element or iterable<etree.Element>
            WFS response containing GML features.

            Can either be a GML `str` or `byte` sequence, in which case it
            will be parsed and scanned for `wfs20:member`.

            Can also be a single instance of `etree.Element` containing the
            parsed GML response.

            It can also be an iterable (list, tuple or generator) of
            `etree.Element` in which case it will be looped over.
        namespace : str
             Namespace associated with this WFS featuretype.

        Yields
        ------
            An instance of this type for each record in the WFS response.

        """
        if isinstance(response, str):
            response = response.encode('utf-8')

        if isinstance(response, bytes):
            response = etree.fromstring(response)

        element_type = type(etree.Element(b'xml'))
        if isinstance(response, element_type):
            feature_members = response.findall(
                './/{http://www.opengis.net/wfs/2.0}member')

            if feature_members is not None:
                for member in feature_members:
                    feature = member[0]
                    yield (cls.from_wfs_element(feature, namespace))

        if type(response) in (list, tuple, set) \
                or isinstance(response, types.GeneratorType):
            for el in response:
                yield (cls.from_wfs_element(el, namespace))

    @classmethod
    def get_field_names(cls, return_fields=None, include_subtypes=True,
                        include_wfs_injected=False, include_geometry=False):
        """Return the names of the fields available for this type.

        Parameters
        ----------
        return_fields : ReturnFieldList
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.
        include_subtypes : boolean
            Whether to include fields defined in subtypes (True) or not (
            False). Defaults to True.
        include_wfs_injected : boolean
            Whether to include fields defined in WFS only, not in the
            default dataframe for this type. Defaults to False.
        include_geometry : boolean
            Whether to include geometry fields. Defaults to False.

        Returns
        -------
        list<str>
            List of the field names available for this type. These are also
            the names of the columns in the output dataframe for this type.

        Raises
        ------
        AttributeError
            If the type of `return_fields` is not one of None, list, tuple or
            set.
        pydov.util.errors.InvalidFieldError
            If at least one of the fields listed in `return_fields` is unknown.

        """
        if return_fields is None:
            if include_wfs_injected:
                fields = [f['name'] for f in cls.fields if f['type']
                          != 'geometry' or include_geometry]
            else:
                fields = [f['name'] for f in cls.fields if not f.get(
                    'wfs_injected', False) and (
                        f['type'] != 'geometry' or include_geometry)]
            if include_subtypes:
                for st in cls.subtypes:
                    fields.extend(st.get_field_names())
        elif not isinstance(return_fields, ReturnFieldList):
            raise AttributeError(
                'return_fields should be an instance of '
                'pydov.types.fields.ReturnFieldList')
        else:
            cls_fields = [f['name'] for f in cls.fields if f['type']
                          != 'geometry' or include_geometry]
            if include_subtypes:
                for st in cls.subtypes:
                    cls_fields.extend(st.get_field_names())

            fields = [f.name for f in return_fields if f.name in cls_fields]

            for rf in return_fields:
                if rf.name not in cls_fields:
                    raise InvalidFieldError(
                        "Unknown return field: '{}'".format(rf.name))
        return fields

    @classmethod
    def get_fields(cls, source=('wfs', 'xml'), include_subtypes=True):
        """Return the metadata of the fields available for this type.

        Parameters
        ----------
        source : list<str> or tuple<str> or iterable<str>
            A list of sources to include in the output. Can be a combination
            of one or more of `wfs`, `xml` or `custom . Defaults to (`wfs`,
            `xml`).
        include_subtypes : boolean
            Whether to include fields defined in subtypes (True) or not (
            False). Defaults to True.

        Returns
        -------
        collections.OrderedDict<str,dict>
            Ordered dictionary mapping the field (column) name to the
            dictionary containing the metadata of this field.

            This metadata dictionary includes at least:

            name (str)
                The name of the field in the output data.

            source (str)
                The source of the field (either `wfs`, `xml` or `custom`).

            type (str)
                Datatype of the output data field (one of `string`, `float`,
                `integer`, `date`, `datetime`, `boolean`).

            split_fn (function)
                Optional, a function to split the value of this field into
                a list of values.

            The metadata dictionary additionally includes for fields with
            source `xml` or `wfs`:

            sourcefield (str)
                The name of the field in the source (source + sourcefield
                identify the origin of the data).

            The metadata dictionary additionally includes for fields with
            source `xml` or `custom`:

            definition (str)
                The definition of the field.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

        """
        fields = OrderedDict(
            zip([f['name'] for f in cls.fields if f['source'] in source],
                [f for f in cls.fields if f['source'] in source]))

        if include_subtypes and 'xml' in source:
            for st in cls.subtypes:
                fields.update(st.get_fields())

        return fields

    @classmethod
    def get_xsd_schemas(cls):
        """Get a set of distinct XSD schema URLs for this type and its
        subtypes.

        Returns
        -------
        set of str
            A set of XSD schema URLs.

        """
        xsd_schemas = set()

        fields = cls.get_fields(source='xml', include_subtypes=True)

        for f in fields.values():
            if 'xsd_type' in f:
                xsd_schemas.add(f['xsd_schema'])

        return xsd_schemas

    @classmethod
    def to_df_array(cls, iterable, return_fields=None):
        """Returns a dataframe array with one or more arrays (rows) for each
        instance in the given iterable.

        Uses parallel processing to speed up IO operations.

        Parameters
        ----------
        iterable : list<DovType> or tuple<DovType> or iterable<DovType>
            A list of instances of a DOV type.
        return_fields : list<str> or tuple<str> or set<str> or iterable<str>
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.

        Returns
        -------
        list of list
            Dataframe contents in the format of a twodimensional list (rows)
            of lists (columns). The values in the second list are in the
            same order as the field/column names, for inclusion in the
            resulting Pandas dataframe of a search operation.

        """
        def unnest_result(result, df_result):
            """Unnest the result into multiple rows (lists) if necessary. Rows
            are appended to the df_result list."""
            if result is not None and len(result) > 0:
                if isinstance(result[0], list):
                    for r in result:
                        df_result.append(r)
                else:
                    df_result.append(result)

        pool = LocalSessionThreadPool()

        for item in iterable:
            pool.execute(item.get_df_array, (return_fields,))

        df_result = []
        for res in pool.join():
            unnest_result(res.get_result(), df_result)

        return df_result

    def _get_xml_data(self, session=None):
        """Return the raw XML data for this DOV object.

        Parameters
        ----------
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        if pydov.cache:
            return pydov.cache.get(self.pkey + '.xml', session)
        else:
            xml = get_dov_xml(self.pkey + '.xml', session)
            HookRunner.execute_xml_downloaded(self.pkey)
            return xml

    def _parse_subtypes(self, xml):
        """Parse the subtypes with the given XML data.

        Parameters
        ----------
        xml : bytes
            The raw XML data of the DOV object as bytes.

        """
        for subtype in self.subtypes:
            st_name = subtype.get_name()
            if st_name not in self.subdata:
                self.subdata[st_name] = []

            for subitem in subtype.from_xml(xml):
                self.subdata[st_name].append(subitem)

    def get_df_array(self, return_fields=None, session=None):
        """Return the data array of the instance of this type for inclusion
        in the resulting output dataframe of a search operation.

        Parameters
        ----------
        return_fields : list<str> or tuple<str> or set<str> or iterable<str>
            List of fields to include in the data array. The order is
            ignored, the default order of the fields of the datatype is used
            instead. Defaults to None, which will include all fields.
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        list
            List of the values of this instance in the same order as the
            field/column names, for inclusion in the result dataframe of a
            search operation.

        """
        fields = self.get_field_names(return_fields, include_geometry=True)
        if len(fields) == 0:
            fields = self.get_field_names(
                return_fields, include_wfs_injected=True,
                include_geometry=False)

        ownfields = self.get_field_names(include_subtypes=False,
                                         include_wfs_injected=True,
                                         include_geometry=True)
        subfields = [f for f in fields if f not in ownfields]
        parsed = None

        if len(subfields) > 0:
            parsed = self._parse_xml_data(session)

        datadicts = []
        datarecords = []

        if len(self.subdata) == 0 or len(subfields) == 0:
            datadicts.append(self.data)
        else:
            for subtype in self.subdata:
                if len(self.subdata[subtype]) == 0:
                    datadicts.append(self.data)
                else:
                    for subdata in self.subdata[subtype]:
                        for subdata_dict in subdata.get_data_dicts():
                            datadict = {}
                            datadict.update(self.data)
                            datadict.update(subdata_dict)
                            datadicts.append(datadict)

        for d in datadicts:
            datarecords.append([d.get(field, np.nan) for field in fields])

        for d in datarecords:
            if parsed is None and self._UNRESOLVED in d:
                parsed = self._parse_xml_data(session)
                if parsed is True:
                    datarecords = self.get_df_array(return_fields)

        return [[c if c != self._UNRESOLVED else np.nan for c in r]
                for r in datarecords]
