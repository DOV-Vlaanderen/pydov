"""Module grouping tests for the pydov.util.owsutil module, without all
module scoped monkeypatches."""
import copy

from pydov.util import owsutil


class TestOwsutilNoMP(object):
    """Class grouping tests for the pydov.util.owsutil module, without all
    module scoped monkeypatches.."""

    def test_get_remote_metadata_nometadataurls(self, wfs):
        """Test the owsutil.get_remote_metadata method when the WFS layer
        missed metadata URLs.

        Test whether None is returned.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        assert owsutil.get_remote_metadata(contentmetadata) is None

    def test_get_remote_metadata_nometadata(self, wfs, mp_geonetwork_broken):
        """Test the owsutil.get_remote_metadata method when the remote metadata
        could not be found.

        Test whether None is returned.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        assert owsutil.get_remote_metadata(contentmetadata) is None
