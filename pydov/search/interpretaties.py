import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.fields import _WfsInjectedField
from pydov.types.interpretaties import FormeleStratigrafie
from pydov.types.interpretaties import InformeleHydrogeologischeStratigrafie
from pydov.types.interpretaties import InformeleStratigrafie
from pydov.types.interpretaties import HydrogeologischeStratigrafie
from pydov.types.interpretaties import LithologischeBeschrijvingen
from pydov.types.interpretaties import GecodeerdeLithologie
from pydov.types.interpretaties import GeotechnischeCodering
from pydov.types.interpretaties import QuartairStratigrafie
from pydov.util import owsutil


class InformeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about 'informele stratigrafie'."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=InformeleStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the InformeleStratigrafie type.
            Optional: defaults to the InformeleStratigrafie type
            containing the fields described in the documentation.

        """
        super(InformeleStratigrafieSearch, self).__init__(
            'interpretaties:informele_stratigrafie', objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if InformeleStratigrafieSearch.__wfs_namespace is None:
            InformeleStratigrafieSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if InformeleStratigrafieSearch.__wfs_schema is None:
                InformeleStratigrafieSearch.__wfs_schema = self._get_schema()

            if InformeleStratigrafieSearch.__md_metadata is None:
                InformeleStratigrafieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if InformeleStratigrafieSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    InformeleStratigrafieSearch.__md_metadata)

                InformeleStratigrafieSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if InformeleStratigrafieSearch.__xsd_schemas is None:
                InformeleStratigrafieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                InformeleStratigrafieSearch.__wfs_schema,
                InformeleStratigrafieSearch.__fc_featurecatalogue,
                InformeleStratigrafieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                InformeleStratigrafieSearch.__wfs_schema,
                InformeleStratigrafieSearch.__fc_featurecatalogue,
                InformeleStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for 'informele stratigrafie'. Provide either `location`
        and/or `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           extra_wfs_fields=['Type_proef', 'Proeffiche'],
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class FormeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve the interpretation for Formele
    stratigrafie"""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=FormeleStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the FormeleStratigrafie type.
            Optional: defaults to the FormeleStratigrafie type containing the
            fields described in the documentation.

        """
        super(FormeleStratigrafieSearch, self).__init__(
            'interpretaties:formele_stratigrafie', objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if FormeleStratigrafieSearch.__wfs_namespace is None:
            FormeleStratigrafieSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if FormeleStratigrafieSearch.__wfs_schema is None:
                FormeleStratigrafieSearch.__wfs_schema = self._get_schema()

            if FormeleStratigrafieSearch.__md_metadata is None:
                FormeleStratigrafieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if FormeleStratigrafieSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    FormeleStratigrafieSearch.__md_metadata)

                FormeleStratigrafieSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if FormeleStratigrafieSearch.__xsd_schemas is None:
                FormeleStratigrafieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                FormeleStratigrafieSearch.__wfs_schema,
                FormeleStratigrafieSearch.__fc_featurecatalogue,
                FormeleStratigrafieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                FormeleStratigrafieSearch.__wfs_schema,
                FormeleStratigrafieSearch.__fc_featurecatalogue,
                FormeleStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for 'formele stratigrafie'. Provide either `location` and/or
        `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           extra_wfs_fields=['Type_proef', 'Proeffiche'],
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class HydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve hydrogeological interpretations """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=HydrogeologischeStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the HydrogeologischeStratigrafie
            type. Optional: defaults to the HydrogeologischeStratigrafie type
            containing the fields described in the documentation.

        """
        super(HydrogeologischeStratigrafieSearch, self).__init__(
            'interpretaties:hydrogeologische_stratigrafie',
            objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if HydrogeologischeStratigrafieSearch.__wfs_namespace is None:
            HydrogeologischeStratigrafieSearch.__wfs_namespace = \
                self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if HydrogeologischeStratigrafieSearch.__wfs_schema is None:
                HydrogeologischeStratigrafieSearch.__wfs_schema = \
                    self._get_schema()

            if HydrogeologischeStratigrafieSearch.__md_metadata is None:
                HydrogeologischeStratigrafieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if HydrogeologischeStratigrafieSearch.__fc_featurecatalogue \
                    is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    HydrogeologischeStratigrafieSearch.__md_metadata)

                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if HydrogeologischeStratigrafieSearch.__xsd_schemas is None:
                HydrogeologischeStratigrafieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                HydrogeologischeStratigrafieSearch.__wfs_schema,
                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue,
                HydrogeologischeStratigrafieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                HydrogeologischeStratigrafieSearch.__wfs_schema,
                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue,
                HydrogeologischeStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for hydrogeological interpretations. Provide either
        `location` and/or `query` and/or `max_features`. When
        `return_fields` is None, all fields
        are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class LithologischeBeschrijvingenSearch(AbstractSearch):
    """Search class to retrieve lithologische beschrijvingen """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=LithologischeBeschrijvingen):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the LithologischeBeschrijvingen
            type. Optional: defaults to the LithologischeBeschrijvingen type
            containing the fields described in the documentation.

        """
        super(LithologischeBeschrijvingenSearch, self).__init__(
            'interpretaties:lithologische_beschrijvingen',
            objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if LithologischeBeschrijvingenSearch.__wfs_namespace is None:
            LithologischeBeschrijvingenSearch.__wfs_namespace = \
                self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if LithologischeBeschrijvingenSearch.__wfs_schema is None:
                LithologischeBeschrijvingenSearch.__wfs_schema = \
                    self._get_schema()

            if LithologischeBeschrijvingenSearch.__md_metadata is None:
                LithologischeBeschrijvingenSearch.__md_metadata = \
                    self._get_remote_metadata()

            if LithologischeBeschrijvingenSearch.__fc_featurecatalogue \
                    is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    LithologischeBeschrijvingenSearch.__md_metadata)

                LithologischeBeschrijvingenSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if LithologischeBeschrijvingenSearch.__xsd_schemas is None:
                LithologischeBeschrijvingenSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                LithologischeBeschrijvingenSearch.__wfs_schema,
                LithologischeBeschrijvingenSearch.__fc_featurecatalogue,
                LithologischeBeschrijvingenSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                LithologischeBeschrijvingenSearch.__wfs_schema,
                LithologischeBeschrijvingenSearch.__fc_featurecatalogue,
                LithologischeBeschrijvingenSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for 'lithologische beschrijvingen'. Provide either
        `location` and/or `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class GecodeerdeLithologieSearch(AbstractSearch):
    """Search class to retrieve gecodeerde lithologie """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=GecodeerdeLithologie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GecodeerdeLithologie type.
            Optional: defaults to the GecodeerdeLithologie type containing
            the fields described in the documentation.

        """
        super(GecodeerdeLithologieSearch, self).__init__(
            'interpretaties:gecodeerde_lithologie',
            objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if GecodeerdeLithologieSearch.__wfs_namespace is None:
            GecodeerdeLithologieSearch.__wfs_namespace = \
                self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if GecodeerdeLithologieSearch.__wfs_schema is None:
                GecodeerdeLithologieSearch.__wfs_schema = \
                    self._get_schema()

            if GecodeerdeLithologieSearch.__md_metadata is None:
                GecodeerdeLithologieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if GecodeerdeLithologieSearch.__fc_featurecatalogue \
                    is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    GecodeerdeLithologieSearch.__md_metadata)

                GecodeerdeLithologieSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if GecodeerdeLithologieSearch.__xsd_schemas is None:
                GecodeerdeLithologieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                GecodeerdeLithologieSearch.__wfs_schema,
                GecodeerdeLithologieSearch.__fc_featurecatalogue,
                GecodeerdeLithologieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                GecodeerdeLithologieSearch.__wfs_schema,
                GecodeerdeLithologieSearch.__fc_featurecatalogue,
                GecodeerdeLithologieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for 'gecodeerde lithologie'. Provide either `location`
        and/or `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class GeotechnischeCoderingSearch(AbstractSearch):
    """Search class to retrieve geotechnische codering """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=GeotechnischeCodering):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GeotechnischeCodering type.
            Optional: defaults to the GeotechnischeCodering type containing
            the fields described in the documentation.

        """
        super(GeotechnischeCoderingSearch, self).__init__(
            'interpretaties:geotechnische_coderingen',
            objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if GeotechnischeCoderingSearch.__wfs_namespace is None:
            GeotechnischeCoderingSearch.__wfs_namespace = \
                self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if GeotechnischeCoderingSearch.__wfs_schema is None:
                GeotechnischeCoderingSearch.__wfs_schema = \
                    self._get_schema()

            if GeotechnischeCoderingSearch.__md_metadata is None:
                GeotechnischeCoderingSearch.__md_metadata = \
                    self._get_remote_metadata()

            if GeotechnischeCoderingSearch.__fc_featurecatalogue \
                    is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    GeotechnischeCoderingSearch.__md_metadata)

                GeotechnischeCoderingSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if GeotechnischeCoderingSearch.__xsd_schemas is None:
                GeotechnischeCoderingSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                GeotechnischeCoderingSearch.__wfs_schema,
                GeotechnischeCoderingSearch.__fc_featurecatalogue,
                GeotechnischeCoderingSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                GeotechnischeCoderingSearch.__wfs_schema,
                GeotechnischeCoderingSearch.__fc_featurecatalogue,
                GeotechnischeCoderingSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for 'geotechnische_codering'. Provide either `location`
        and/or `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : tuple<minx,miny,maxx,maxy>
            The bounding box limiting the features to retrieve.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = self._type.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class QuartairStratigrafieSearch(AbstractSearch):
    """Search class to retrieve the interpretation for Quartair
    stratigrafie"""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=QuartairStratigrafie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the QuartairStratigrafie type.
            Optional: defaults to the QuartairStratigrafie type containing
            the fields described in the documentation.

        """
        super(QuartairStratigrafieSearch, self).__init__(
            'interpretaties:quartaire_stratigrafie', objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if QuartairStratigrafieSearch.__wfs_namespace is None:
            QuartairStratigrafieSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if QuartairStratigrafieSearch.__wfs_schema is None:
                QuartairStratigrafieSearch.__wfs_schema = self._get_schema()

            if QuartairStratigrafieSearch.__md_metadata is None:
                QuartairStratigrafieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if QuartairStratigrafieSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    QuartairStratigrafieSearch.__md_metadata)

                QuartairStratigrafieSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if QuartairStratigrafieSearch.__xsd_schemas is None:
                QuartairStratigrafieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                QuartairStratigrafieSearch.__wfs_schema,
                QuartairStratigrafieSearch.__fc_featurecatalogue,
                QuartairStratigrafieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                QuartairStratigrafieSearch.__wfs_schema,
                QuartairStratigrafieSearch.__fc_featurecatalogue,
                QuartairStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for interpretations of Quartair stratigrafie.

        Provide either `location` and/or `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = self._type.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(interpretaties, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df


class InformeleHydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about informele
    hydrogeologische stratigrafie.

    Parameters
    ----------
    objecttype : subclass of pydov.types.abstract.AbstractDovType
        Reference to a class representing the
        InformeleHydrogeologischeStratigrafie type.
        Optional: defaults to the InformeleHydrogeologischeStratigrafie type
        containing the fields described in the documentation.

    """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=InformeleHydrogeologischeStratigrafie):
        """Initialisation."""
        super(InformeleHydrogeologischeStratigrafieSearch, self).__init__(
            'interpretaties:informele_hydrogeologische_stratigrafie',
            objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if InformeleHydrogeologischeStratigrafieSearch.__wfs_namespace is None:
            InformeleHydrogeologischeStratigrafieSearch.__wfs_namespace = \
                self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if InformeleHydrogeologischeStratigrafieSearch.__wfs_schema is \
                    None:
                InformeleHydrogeologischeStratigrafieSearch.__wfs_schema = \
                    self._get_schema()

            if InformeleHydrogeologischeStratigrafieSearch.__md_metadata is \
                    None:
                InformeleHydrogeologischeStratigrafieSearch.__md_metadata = \
                    self._get_remote_metadata()

            if InformeleHydrogeologischeStratigrafieSearch.\
                    __fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    InformeleHydrogeologischeStratigrafieSearch.__md_metadata)

                InformeleHydrogeologischeStratigrafieSearch.\
                    __fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if InformeleHydrogeologischeStratigrafieSearch.__xsd_schemas is \
                    None:
                InformeleHydrogeologischeStratigrafieSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                InformeleHydrogeologischeStratigrafieSearch.__wfs_schema,
                InformeleHydrogeologischeStratigrafieSearch.
                __fc_featurecatalogue,
                InformeleHydrogeologischeStratigrafieSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                InformeleHydrogeologischeStratigrafieSearch.__wfs_schema,
                InformeleHydrogeologischeStratigrafieSearch.
                __fc_featurecatalogue,
                InformeleHydrogeologischeStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for boreholes (Boring). Provide either `location` or `query`.
        When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location` or `query` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        interpretaties = InformeleHydrogeologischeStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=InformeleHydrogeologischeStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=InformeleHydrogeologischeStratigrafie.get_field_names(
                return_fields))
        return df
