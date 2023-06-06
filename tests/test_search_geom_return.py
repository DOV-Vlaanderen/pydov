"""Module grouping tests for returning geometry fields."""
import geopandas as gpd
from shapely.geometry import Point

from pydov.search.bodemclassificatie import BodemclassificatieSearch

location_md_metadata = 'tests/data/types/bodemclassificatie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemclassificatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemclassificatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemclassificatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemclassificatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemclassificatie/bodemclassificatie.xml'
location_xsd_base = 'tests/data/types/bodemclassificatie/xsd_*.xml'


class TestGeometryReturn(object):
    """Class grouping tests for returning geometry fields."""

    def test_return_geometry(self, mp_get_schema,
                             mp_remote_describefeaturetype,
                             mp_remote_wfs_feature):
        """Test whether the geometry field is returned when requested.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        """
        return_fields = [
            'pkey_bodemclassificatie', 'pkey_bodemlocatie', 'x', 'y', 'mv_mtaw',
            'classificatietype', 'bodemtype', 'auteurs', 'geom'
        ]

        s = BodemclassificatieSearch()
        df = s.search(max_features=1, return_fields=return_fields)

        assert 'geom' in list(df)
        assert len(df.geom.notna()) == 1
        assert Point(248905.6718, 200391.287).equals_exact(df.geom[0], tolerance=0.01)

    def test_to_geopandas(self, mp_get_schema,
                          mp_remote_describefeaturetype,
                          mp_remote_wfs_feature):
        """Test whether the resulting dataframe can be turned into a GeoPandas GeoDataFrame.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        """
        return_fields = [
            'pkey_bodemclassificatie', 'pkey_bodemlocatie', 'x', 'y', 'mv_mtaw',
            'classificatietype', 'bodemtype', 'auteurs', 'geom'
        ]

        s = BodemclassificatieSearch()
        df = s.search(max_features=1, return_fields=return_fields)

        geo_df = gpd.GeoDataFrame(df, geometry='geom', crs='EPSG:31370')
        assert isinstance(geo_df, gpd.GeoDataFrame)
