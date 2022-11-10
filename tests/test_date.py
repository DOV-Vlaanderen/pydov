"""Tests regarding dates and timestamps."""

import pytest
import numpy as np

from tests.test_search_grondwatervergunning import (
    location_md_metadata, location_fc_featurecatalogue,
    location_wfs_describefeaturetype, location_xsd_base
)

from pydov.search.grondwatervergunning import GrondwaterVergunningSearch
from pydov.util.errors import DataParseWarning

location_wfs_getfeature = 'tests/data/date/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/date/feature.xml'


class TestSearchInvalidDate(object):
    """Test the behaviour when encoutering invalid dates in the data."""

    def test_year_gt_9999(self, mp_wfs, mp_get_schema,
                          mp_remote_describefeaturetype, mp_remote_md,
                          mp_remote_fc, mp_remote_wfs_feature):
        """Test with a year greater than 9999. This is not supported in Python.

        Test whether no exception is raised, but instead the date is replaced with NaN and a warning is raised.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        """
        s = GrondwaterVergunningSearch()

        with pytest.warns(DataParseWarning):
            df = s.search(max_features=1)
            assert np.isnan(df.tot_datum_termijn.iloc[0])
