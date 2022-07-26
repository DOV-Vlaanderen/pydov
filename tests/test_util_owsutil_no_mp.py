"""Module grouping tests for the pydov.util.owsutil module, without all
module scoped monkeypatches."""
import copy

import pytest

from pydov.util import owsutil
from pydov.util.errors import MetadataNotFoundError


class TestOwsutilNoMP(object):
    """Class grouping tests for the pydov.util.owsutil module, without all
    module scoped monkeypatches.."""

    def test_get_remote_metadata_nometadataurls(self, wfs):
        """Test the owsutil.get_remote_metadata method when the WFS layer
        missed metadata URLs.

        Test whether a MetadataNotFoundError is raised.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_remote_metadata(contentmetadata)
