"""Module grouping online tests for returning geometry fields."""
from owslib.fes2 import PropertyIsEqualTo
import pytest
from shapely.geometry import Point

from pydov.search.bodemclassificatie import BodemclassificatieSearch
from pydov.types.fields import GeometryReturnField
from pydov.util.dovutil import build_dov_url
from tests.abstract import ServiceCheck


class TestGeometryReturnOnline(object):
    """Class grouping online tests for returning geometry fields."""

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_return_geometry_4326(self):
        """Test whether the geometry field is returned in the correct SRS.

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
            'classificatietype', 'bodemtype', 'auteurs', GeometryReturnField('geom', 4326)
        ]

        s = BodemclassificatieSearch()
        df = s.search(query=PropertyIsEqualTo(
            propertyname='pkey_bodemclassificatie',
            literal=build_dov_url('data/belgischebodemclassificatie/2018-000146')),
            return_fields=return_fields)

        assert 'geom' in list(df)
        assert len(df.geom.notna()) == 1
        assert Point(5.781, 51.10514).equals_exact(df.geom[0], tolerance=0.01)
