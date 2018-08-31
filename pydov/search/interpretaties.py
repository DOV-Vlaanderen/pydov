import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.interpretaties import InformeleStratigrafie
from pydov.types.interpretaties import HydrogeologischeStratigrafie
from pydov.util import owsutil


class InformeleStratigrafieSearch(AbstractSearch):
    """Search class to retrieve information about boreholes (Boring)."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None

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

            fields = self._build_fields(
                InformeleStratigrafieSearch.__wfs_schema,
                InformeleStratigrafieSearch.__fc_featurecatalogue)

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
                InformeleStratigrafieSearch.__fc_featurecatalogue)

    def search(self, location=None, query=None, return_fields=None):
        """Search for boreholes (Boring). Provide either `location` or `query`.
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


class HydrogeologischeStratigrafieSearch(AbstractSearch):
    """Search class to retrieve hydrogeological interpretations """

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None

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

            fields = self._build_fields(
                HydrogeologischeStratigrafieSearch.__wfs_schema,
                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue)

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
                HydrogeologischeStratigrafieSearch.__fc_featurecatalogue)

    def search(self, location=None, query=None, return_fields=None):
        """Search for hydrogeological interpretations. Provide either
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
                           return_fields=return_fields,
                           extra_wfs_fields=['Type_proef', 'Proeffiche'])

        interpretaties = HydrogeologischeStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=HydrogeologischeStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=HydrogeologischeStratigrafie.get_field_names(
                return_fields))
        return df
