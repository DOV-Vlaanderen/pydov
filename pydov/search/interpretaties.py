import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.interpretaties import FormeleStratigrafie
from pydov.types.interpretaties import InformeleStratigrafie
from pydov.types.interpretaties import HydrogeologischeStratigrafie
from pydov.types.interpretaties import LithologischeBeschrijvingen
from pydov.types.interpretaties import GecodeerdeLithologie
from pydov.types.interpretaties import GeotechnischeCodering
from pydov.util import owsutil


class InformeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about boreholes (Boring)."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(InformeleStratigrafieSearch, self).__init__(
            'interpretaties:informele_stratigrafie', InformeleStratigrafie)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                InformeleStratigrafieSearch.__wfs_schema,
                InformeleStratigrafieSearch.__fc_featurecatalogue,
                InformeleStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields,
                           extra_wfs_fields=['Type_proef', 'Proeffiche'])

        interpretaties = InformeleStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=InformeleStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=InformeleStratigrafie.get_field_names(return_fields))
        return df


class FormeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve the interpretation for Formele
    stratigrafie"""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(FormeleStratigrafieSearch, self).__init__(
            'interpretaties:formele_stratigrafie', FormeleStratigrafie)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                FormeleStratigrafieSearch.__wfs_schema,
                FormeleStratigrafieSearch.__fc_featurecatalogue,
                FormeleStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields,
                           extra_wfs_fields=['Type_proef', 'Proeffiche'])

        interpretaties = FormeleStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=FormeleStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=FormeleStratigrafie.get_field_names(return_fields))
        return df


class HydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve hydrogeological interpretations """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(HydrogeologischeStratigrafieSearch, self).__init__(
            'interpretaties:hydrogeologische_stratigrafie',
            HydrogeologischeStratigrafie)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                HydrogeologischeStratigrafieSearch.__wfs_schema,
                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue,
                HydrogeologischeStratigrafieSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
        """Search for hydrogeological interpretations. Provide either
        `location` or `query`. When `return_fields` is None, all fields
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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        interpretaties = HydrogeologischeStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=HydrogeologischeStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=HydrogeologischeStratigrafie.get_field_names(
                return_fields))
        return df


class LithologischeBeschrijvingenSearch(AbstractSearch):
    """Search class to retrieve lithologische beschrijvingen """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(LithologischeBeschrijvingenSearch, self).__init__(
            'interpretaties:lithologische_beschrijvingen',
            LithologischeBeschrijvingen)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                LithologischeBeschrijvingenSearch.__wfs_schema,
                LithologischeBeschrijvingenSearch.__fc_featurecatalogue,
                LithologischeBeschrijvingenSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
        """Search for 'lithologische beschrijvingen'. Provide either
        `location` or `query`. When `return_fields` is None, all fields
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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        interpretaties = LithologischeBeschrijvingen.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=LithologischeBeschrijvingen.to_df_array(
                interpretaties, return_fields),
            columns=LithologischeBeschrijvingen.get_field_names(
                return_fields))
        return df


class GecodeerdeLithologieSearch(AbstractSearch):
    """Search class to retrieve gecodeerde lithologie """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(GecodeerdeLithologieSearch, self).__init__(
            'interpretaties:gecodeerde_lithologie',
            GecodeerdeLithologie)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                GecodeerdeLithologieSearch.__wfs_schema,
                GecodeerdeLithologieSearch.__fc_featurecatalogue,
                GecodeerdeLithologieSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
        """Search for 'gecodeerde lithologie'. Provide either
        `location` or `query`. When `return_fields` is None, all fields
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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        interpretaties = GecodeerdeLithologie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=GecodeerdeLithologie.to_df_array(
                interpretaties, return_fields),
            columns=GecodeerdeLithologie.get_field_names(
                return_fields))
        return df


class GeotechnischeCoderingSearch(AbstractSearch):
    """Search class to retrieve geotechnische codering """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(GeotechnischeCoderingSearch, self).__init__(
            'interpretaties:geotechnische_coderingen',
            GeotechnischeCodering)

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
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                GeotechnischeCoderingSearch.__wfs_schema,
                GeotechnischeCoderingSearch.__fc_featurecatalogue,
                GeotechnischeCoderingSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
        """Search for 'geotechnische_codering'. Provide either
        `location` or `query`. When `return_fields` is None, all fields
        are returned.

        Parameters
        ----------
        location : tuple<minx,miny,maxx,maxy>
            The bounding box limiting the features to retrieve.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        interpretaties = GeotechnischeCodering.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=GeotechnischeCodering.to_df_array(
                interpretaties, return_fields),
            columns=GeotechnischeCodering.get_field_names(
                return_fields))
        return df
