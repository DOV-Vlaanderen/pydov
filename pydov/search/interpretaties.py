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

            if HydrogeologischeStratigrafieSearch.__fc_featurecatalogue is None:
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

        interpretaties = HydrogeologischeStratigrafie.from_wfs(
            fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=HydrogeologischeStratigrafie.to_df_array(
                interpretaties, return_fields),
            columns=HydrogeologischeStratigrafie.get_field_names(return_fields))
        return df


if __name__ == '__main__':
    import os, sys
    import numpy as np
    import inspect
    # check pydov path
    import pydov
    print(pydov.__path__)
    from pydov.search.interpretaties import InformeleStratigrafieSearch
    from pydov.search.interpretaties import HydrogeologischeStratigrafieSearch
    ip_infstrat = InformeleStratigrafieSearch()
    ip_hydrogeo = HydrogeologischeStratigrafieSearch()


    """
    # information about the HydrogeologischeStratigrafie type (In Dutch):
    print(ip_infstrat.get_description())
    # information about the available fields for a HydrogeologischeStratigrafie object
    fields = ip_infstrat.get_fields()
    # print available fields
    for f in fields.values():
        print(f['name'])
    # df = ip_hydrogeo.search(location=(31020, 131890, 260900, 166610))
    df_hydrogeo_wal = pd.read_csv(
        os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                     'df_hydrogeo_waltemp.csv'),
        dtype={'pkey_interpretatie': object, 'pkey_boring': object, 'pkey_sondering': object,
               'betrouwbaarheid_interpretatie': object, 'diepte_laag_van': float,
               'diepte_laag_tot': float, 'aquifer': str})



    import folium
    from pyproj import Proj, transform

    from pydov.search.boring import BoringSearch
    from owslib.fes import PropertyIsLike

    boring = BoringSearch()
    df_borehole = pd.DataFrame([])
    for idx, rec in df_hydrogeo_wal.iterrows():
        query = PropertyIsLike(propertyname='fiche', literal=rec.pkey_boring)
        df_borehole = df_borehole.append(boring.search(query=query))

    # read csv if already obtained
    df_boring = pd.read_csv(
        os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                     'df_boring.csv'))
    df_hydrogeo = pd.read_csv(
        os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                     'df_hydrogeo.csv'),
        dtype={'pkey_interpretatie': object, 'pkey_boring': object, 'pkey_sondering': object,
               'betrouwbaarheid_interpretatie': object, 'diepte_laag_van': float,
               'diepte_laag_tot': float, 'aquifer': str})

    df_b = df_boring.append(df_borehole)
    df_hydrogeo_b = df_hydrogeo.append(df_hydrogeo_wal)
    df_b.drop_duplicates(subset='pkey_boring', inplace=True)
    df_hydrogeo_b.drop_duplicates(subset=['pkey_boring', 'aquifer'], inplace=True)
    df_join = pd.merge(df_b, df_hydrogeo_b, on='pkey_boring')
    df_join.to_csv(os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                                'df_join.csv'))
    """
    # limit to bottom of HCOV unit
    df_join = pd.read_csv(
        os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                     'df_join.csv'))

    # recalculate mtaw
    df_join['tot_mtaw'] = df_join['mv_mtaw'] - df_join['diepte_laag_tot']
    df_join['van_mtaw'] = df_join['mv_mtaw'] - df_join['diepte_laag_van']

    df_join['hcov_main'] = df_join['aquifer'] // 100

    def check_bottom_interpretation(df, hcov_col='aquifer', bottom_col='tot_mtaw'):
        """

        :param df:
        :return:
        """
        # select lowest 'tot_mtaw'
        df_min = df.groupby(hcov_col).agg({bottom_col: 'min'})
        codes = sorted(df_min.index.values)
        df['interpret_bottom'] = -999.
        for code in codes:
            # catch 0000 and 0100 because no top guaranteed
            if code <= 1:
                continue
            df.loc[df[hcov_col] == code, 'interpret_bottom'] = df_min.loc[codes[codes.index(code) - 1], bottom_col]
        return df

    # drop na of bottom col
    df_join.dropna(subset=['tot_mtaw', 'hcov_main'], inplace=True)
    df_join['interpret_bottom'] = pd.DataFrame(index=df_join.index, columns=['interpret_bottom'])
    df_join = df_join.groupby(['pkey_interpretatie']).apply(check_bottom_interpretation,
                                                       hcov_col='hcov_main', bottom_col='tot_mtaw')
    a = 1

    df_join.to_csv(os.path.join(r'Z:\AGT\ProjectenAGT\1310-Advies en review voor NIRAS\TECH-GEGEVENS\2017-2020\DATA\PJ',
                                'df_join_bottoms.csv'))


    def convert_latlon(x1, y1):
        inProj = Proj(init='epsg:31370')
        outProj = Proj(init='epsg:4326')
        x2, y2 = transform(x1, y1)
        return x2, y2


    df['lon'], df['lat'] = zip(*map(convert_latlon, df['x'], df['y']))

    a = 'stop'

