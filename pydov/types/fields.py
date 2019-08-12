"""Module grouping all classes related to pydov field definitions."""


class XsdType(object):
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
    def __init__(self, name, source, datatype, **kwargs):
        """Initialise a field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source: one of 'wfs', 'xml'
            Source of this field.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime'
                or 'boolean'
            Datatype of the values of this field in the return dataframe.

        """
        super(AbstractField, self).__init__(**kwargs)
        self.__setitem__('name', name)
        self.__setitem__('source', source)
        self.__setitem__('type', datatype)


class WfsField(AbstractField):
    def __init__(self, name, source_field, datatype):
        """Initialse a WFS field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source_field : str
            Name of this field in the source WFS service.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime'
                or 'boolean'
            Datatype of the values of this field in the return dataframe.

        """
        super(WfsField, self).__init__(name, 'wfs', datatype)
        self.__setitem__('sourcefield', source_field)


class WfsInjectedField(WfsField):
    def __init__(self, name, datatype):
        """Initialise a WFS injected field.

        This is a field not normally present in the dataframe, but useable as
        a query and returnfield as it is available in the WFS service.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime'
                or 'boolean'
            Datatype of the values of this field in the return dataframe.

        """
        super(WfsInjectedField, self).__init__(name, name, datatype)
        self.__setitem__('wfs_injected', True)


class XmlField(AbstractField):
    def __init__(self, name, source_xpath, definition, datatype, notnull,
                 xsd_type=None):
        """Initialise an XML field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        source_xpath : str
            XPath expression of the values of this field in the source XML
            document.
        definition : str
            Definition of this field.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime'
                or 'boolean'
            Datatype of the values of this field in the return dataframe.
        notnull : bool
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


class CustomField(AbstractField):
    def __init__(self, name, definition, datatype, notnull):
        """Initialise a custom field.

        Parameters
        ----------
        name : str
            Name of this field in the return dataframe.
        definition : str
            Definition of this field.
        datatype : one of 'string', 'integer', 'float', 'date', 'datetime'
                or 'boolean'
            Datatype of the values of this field in the return dataframe.
        notnull : bool
            True if this field is always present (mandatory), False otherwise.

        """
        super(CustomField, self).__init__(name, 'custom', datatype)
        self.__setitem__('definition', definition)
        self.__setitem__('notnull', notnull)
