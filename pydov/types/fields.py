# -*- coding: utf-8 -*-
"""Module grouping all classes related to pydov field definitions."""


class AbstractField(dict):
    """Abstract base class for pydov field definitions. Not to be
    instantiated directly."""

    def __init__(self, name, source, datatype, split_fn=None, codelist=None,
                 **kwargs):
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
        codelist : pydov.util.codelists.AbstractCodeList, optional
            Codelist associated with this field.

        """
        super(AbstractField, self).__init__(**kwargs)
        self.__setitem__('name', name)
        self.__setitem__('source', source)
        self.__setitem__('type', datatype)
        self.__setitem__('split_fn', split_fn)
        self.__setitem__('codelist', codelist)


class WfsField(AbstractField):
    """Class for a field available in the WFS service."""

    def __init__(self, name, source_field, datatype, split_fn=None,
                 codelist=None):
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
        codelist : pydov.util.codelists.AbstractCodeList, optional
            Codelist associated with this field.

        """
        super(WfsField, self).__init__(name, 'wfs', datatype, split_fn,
                                       codelist)
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
                 notnull=False, codelist=None):
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
        codelist : pydov.util.codelists.AbstractCodeList, optional
            Codelist associated with this field.

        """
        super(XmlField, self).__init__(
            name=name, source='xml', datatype=datatype, split_fn=None,
            codelist=codelist)

        self.__setitem__('sourcefield', source_xpath)
        self.__setitem__('definition', definition)
        self.__setitem__('notnull', notnull)


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

