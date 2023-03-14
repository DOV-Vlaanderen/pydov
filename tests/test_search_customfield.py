import pandas as pd
import pytest
from pydov.search.interpretaties import InformeleStratigrafieSearch

from tests.abstract import ServiceCheck


class TestSearchCustomWfsField(object):
    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_search_resolve_customfield(self):
        """Test the search method without explicitly requesting the
            'Type_proef' and 'Proeffiche' fields.

            Test whether the output dataframe includes values for pkey_boring or
            pkey_sondering.

            Parameters
            ----------
            mp_get_schema : pytest.fixture
                Monkeypatch the call to a remote OWSLib schema.
            mp_remote_describefeaturetype : pytest.fixture
                Monkeypatch the call to a remote DescribeFeatureType .
            mp_remote_wfs_feature : pytest.fixture
                Monkeypatch the call to get WFS features.
            mp_dov_xml : pytest.fixture
                Monkeypatch the call to get the remote XML data.

            """
        df = InformeleStratigrafieSearch().search(
            max_features=1,
            return_fields=('pkey_interpretatie', 'pkey_boring',
                           'pkey_sondering'))

        assert (not pd.isnull(df.pkey_boring[0])) or (
            not pd.isnull(df.pkey_sondering[0]))
