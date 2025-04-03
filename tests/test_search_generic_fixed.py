"""Module grouping tests for the generic search module, using fixed testdata."""

from pydov.search.generic import WfsSearch

location_md_metadata = \
    'tests/data/types/generic/fixed/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/generic/fixed/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/generic/fixed/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/generic/fixed/' \
                          'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/generic/fixed/feature.xml'
location_dov_xml = None
location_xsd_base = 'tests/data/types/generic/fixed/xsd_*.xml'


class TestWfsSearchFixed:
    def test_get_fields_missing_from_fc(
            self, mp_wfs, mp_get_schema,
            mp_remote_describefeaturetype, mp_remote_md,
            mp_remote_fc, mp_remote_xsd):
        """Test whether fields that are missing from the feature catalogue are
        still included in the get_fields."""

        s = WfsSearch('pfas:pfas_analyseresultaten')
        fields = s.get_fields()
        assert 'x_ml72' in fields

    def test_output_fields_missing_from_fc(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
            mp_dov_xml):
        """Test whether fields that are missing from the feature catalogue are
        still included in the output."""

        s = WfsSearch('pfas:pfas_analyseresultaten')
        df = s.search(max_features=1)
        assert 'x_ml72' in list(df)
