# -*- coding: utf-8 -*-
"""Module grouping all classes related to pydov field definitions."""


class XsdType(object):
    """Class for specifying an XSD type from an XSD schema. This will be
    resolved at runtime in a list of possible values and their definitions."""

    def __init__(self, xsd_schema, typename):
        """Initialise a XSD type reference.

        Parameters
        ----------
        xsd_schema : str
            URL of XSD schema record containing the specified typename.
        typename : str
            Name of the type.

        """
        self.xsd_schema = xsd_schema
        self.typename = typename


class AbstractField(dict):
    """Abstract base class for pydov field definitions. Not to be
    instantiated directly."""

    def __init__(self, name, source, datatype, split_fn=None, **kwargs):
        """Initialise a field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source : one of 'wfs', 'xml', 'custom_wfs', 'custom_xml'
            Source of this field.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.
        split_fn : optional, function
            Function to split values from this field into a list of values.

        """
        super(AbstractField, self).__init__(**kwargs)
        self.__setitem__('name', name)
        self.__setitem__('source', source)
        self.__setitem__('type', datatype)
        self.__setitem__('split_fn', split_fn)


class WfsField(AbstractField):
    """Class for a field available in the WFS service."""

    def __init__(self, name, source_field, datatype, split_fn=None):
        """Initialise a WFS field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source_field : str
            Name of this field in the source WFS service.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.
        split_fn : optional, function
            Function to split values from this field into a list of values.

        """
        super(WfsField, self).__init__(name, 'wfs', datatype, split_fn)
        self.__setitem__('sourcefield', source_field)


class _WfsInjectedField(WfsField):
    """Class for a field available in the WFS service, but not included in the
    default dataframe output."""

    def __init__(self, name, datatype):
        """Initialise a WFS injected field.

        This is a field not normally present in the dataframe, but usable as
        a query and returnfield as it is available in the WFS service.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.

        """
        super(_WfsInjectedField, self).__init__(name, name, datatype)
        self.__setitem__('wfs_injected', True)


class XmlField(AbstractField):
    """Class for a field available in the XML document."""

    def __init__(self, name, source_xpath, datatype, definition='',
                 notnull=False, xsd_type=None):
        """Initialise an XML field.

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
        definition : str, optional
            Definition of this field.
        notnull : bool, optional, defaults to False
            True if this field is always present (mandatory), False otherwise.
        xsd_type : pydov.types.abstract.XsdType, optional
            XSD type associated with this field.

        """
        super(XmlField, self).__init__(name, 'xml', datatype)

        self.__setitem__('sourcefield', source_xpath)
        self.__setitem__('definition', definition)
        self.__setitem__('notnull', notnull)

        if xsd_type is not None:
            self.__setitem__('xsd_schema', xsd_type.xsd_schema)
            self.__setitem__('xsd_type', xsd_type.typename)


class _CustomWfsField(AbstractField):
    """Class for a custom field, created explicitly in pydov from other WFS
    fields."""

    def __init__(self, name, datatype, definition='', notnull=False):
        """Initialise a custom field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.
        definition : str, optional
            Definition of this field.
        notnull : bool, optional, defaults to False
            True if this field is always present (mandatory), False otherwise.

        """
        super(_CustomWfsField, self).__init__(name, 'custom_wfs', datatype)
        self.__setitem__('definition', definition)
        self.__setitem__('notnull', notnull)

    def requires_wfs_fields(self):
        """Get a list of WFS fields that are required by (the calculation of)
        this custom field.

        Returns
        -------
        list of str
            List of WFS fieldnames that is required by this custom field.

        Raises
        ------
        NotImplementedError
            Implement this in a subclass.
        """
        raise NotImplementedError

    def calculate(self, instance):
        """Calculate the value of this custom field for the given instance.

        Parameters
        ----------
        instance : AbstractDovType
            Instance of the corresponding type, containing all WFS values in
            its data dictionary.

        Returns
        -------
        Value to be used for this custom field for this instance. Its datatype
        should match the one set in the initialisation of the custom field.

        Raises
        ------
        NotImplementedError
            Implement this in a subclass.
        """
        raise NotImplementedError


class _CustomXmlField(AbstractField):
    """Class for a custom field, created explicitly in pydov from other XML
    fields."""

    def __init__(self, name, datatype, definition='', notnull=False):
        """Initialise a custom field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime' \
                   or 'boolean'
            Datatype of the values of this field in the return dataframe.
        definition : str, optional
            Definition of this field.
        notnull : bool, optional, defaults to False
            True if this field is always present (mandatory), False otherwise.

        """
        super(_CustomXmlField, self).__init__(name, 'custom_xml', datatype)
        self.__setitem__('definition', definition)
        self.__setitem__('notnull', notnull)

    def calculate(self, cls, tree):
        """Calculate the value of this custom field from the given XML tree.

        Parameters
        ----------
        cls : AbstractDovType
            Class of the type this field belongs to.
        tree : etree.ElementTree
            ElementTree of the DOV XML for this instance.

        Returns
        -------
        Value to be used for this custom field for this instance. Its datatype
        should match the one set in the initialisation of the custom field.

        Raises
        ------
        NotImplementedError
            Implement this in a subclass.
        """
        raise NotImplementedError


class ReturnFieldList(list):
    """List of return fields used in search methods. """

    def __contains__(self, __key: object):
        """Overwrite the default method. Checks on field name.

        Parameters
        ----------
        __key
            The key to check.

        Returns
        -------
        boolean
            Whether the key is one of the names in the ReturnFieldList.
        """
        return __key in [i.name for i in self]

    def get_names(self):
        """Return a list with all the names of the fields in this
        ReturnFieldList.

        Returns
        -------
        list of str
            List of field names.
        """
        return [f.name for f in self]

    @classmethod
    def from_field_names(self, *return_fields):
        """Initiale a ReturnFieldList from a list of return field names.

        Parameters
        ----------
        return_fields : list or set or tuple of str
            List, set or tuple of return field names.

        Returns
        -------
        ReturnFieldList
            Equivalent ReturnFieldList.

        Raises
        ------
        AttributeError
            If the value of return_fields is not a list, set or tuple.
        """
        if len(return_fields) == 0:
            return None

        if len(return_fields) == 1:
            return_fields = return_fields[0]

        if isinstance(return_fields, str):
            return_fields = (return_fields,)

        if return_fields is None:
            return None

        if not isinstance(return_fields, (list, set, tuple)):
            # FIXME: this should be TypeError instead
            raise AttributeError(
                'return_fields should be a list, set or tuple')

        result = ReturnFieldList()
        for rf in return_fields:
            if isinstance(rf, AbstractReturnField):
                result.append(rf)
            else:
                result.append(ReturnField.from_field_name(rf))
        return result


class AbstractReturnField:
    """Base class of ReturnField and GeometryReturnField."""

    def __init__(self, name):
        """Initialisation.

        Parameters
        ----------
        name : str
            Name of the return field.
        """
        self.name = name

    @classmethod
    def from_field_name(cls, name):
        """Initialise a new instance from a field name.

        Parameters
        ----------
        name : str
            Field name.

        Returns
        -------
        Instance of this class.
            Instance of ReturnField or GeometryReturnField.
        """
        return cls(name)


class ReturnField(AbstractReturnField):
    """Normal (non-geometry) return field."""

    def __init__(self, name):
        """Initialisation.

        Parameters
        ----------
        name : str
            Name of the return field.
        """
        super().__init__(name)


class GeometryReturnField(AbstractReturnField):
    def __init__(self, geometry_field, epsg=None):
        """Initialise a geometry return field.

        Parameters
        ----------
        geometry_field : str
            Name of the geometry field.
        epsg : int, optional
            EPSG code of the CRS of the geometries that will be returned.
            Defaults to None, which means the default CRS of the WFS layer.
        """
        super().__init__(geometry_field)

        if epsg is not None:
            if not isinstance(epsg, int):
                raise TypeError('epsg should be an integer value')

        self.epsg = epsg
