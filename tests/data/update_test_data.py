"""Script to update the testdata based on DOV webservices."""
import sys

from owslib.etree import etree
from owslib.util import openURL

from pydov.types.boring import Boring
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.types.interpretaties import (
    GeotechnischeCodering,
    GecodeerdeLithologie,
    LithologischeBeschrijvingen,
    HydrogeologischeStratigrafie,
    FormeleStratigrafie,
    InformeleStratigrafie,
)
from pydov.types.sondering import Sondering


def get_first_featuremember(wfs_response):
    tree = etree.fromstring(wfs_response.encode('utf-8'))

    feature_members = tree.find('.//{http://www.opengis.net/gml}'
                                'featureMembers')

    if feature_members is not None:
        for ft in feature_members:
            return etree.tostring(ft).decode('utf-8')


def update_file(filepath, url, process_fn=None):
    sys.stdout.write('Updating %s ...' % filepath)
    try:
        data = openURL(url).read()
        if type(data) is bytes:
            data = data.decode('utf-8')
    except Exception as e:
        sys.stdout.write(' FAILED:\n   %s.\n' % e)
        return
    else:
        with open(filepath, 'wb') as f:
            if process_fn:
                data = process_fn(data)
            f.write(data.encode('utf-8'))
            sys.stdout.write(' OK.\n')


if __name__ == '__main__':
    # types/boring

    update_file('types/boring/boring.xml',
                'https://www.dov.vlaanderen.be/data/boring/2004-103984.xml')

    update_file('types/boring/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub:Boringen'
                '&maxFeatures=1&CQL_Filter=fiche=%27https://www.dov'
                '.vlaanderen.be/data/boring/2004-103984%27')

    update_file('types/boring/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub:Boringen'
                '&maxFeatures=1&CQL_Filter=fiche=%27https://www.dov'
                '.vlaanderen.be/data/boring/2004-103984%27',
                get_first_featuremember)

    update_file('types/boring/fc_featurecatalogue.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=c0cbd397-520f-4ee1-aca7-d70e271eeed6')

    update_file('types/boring/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=4e20bf9c-3a5c-42be-b5b6-bef6214d1fa7')

    update_file('types/boring/wfsdescribefeaturetype.xml',
                'https://www.dov.vlaanderen.be/geoserver/dov-pub/Boringen'
                '/ows?service=wfs&version=1.1.0&request=DescribeFeatureType')

    for xsd_schema in Boring.get_xsd_schemas():
        update_file(
            'types/boring/xsd_%s.xml' % xsd_schema.split('/')[-1],
            xsd_schema)

    # types/sondering

    update_file('types/sondering/sondering.xml',
                'https://www.dov.vlaanderen.be/data/sondering/2002-018435.xml')

    update_file('types/sondering/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub'
                ':Sonderingen&maxFeatures=1&CQL_Filter=fiche=%27https://www.'
                'dov.vlaanderen.be/data/sondering/2002-018435%27')

    update_file('types/sondering/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub'
                ':Sonderingen&maxFeatures=1&CQL_Filter=fiche=%27https://www.'
                'dov.vlaanderen.be/data/sondering/2002-018435%27',
                get_first_featuremember)

    update_file('types/sondering/fc_featurecatalogue.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=bd539ba5-5f4d-4c43-9662-51c16caea351')

    update_file('types/sondering/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=b397faec-1b64-4854-8000-2375edb3b1a8')

    update_file('types/sondering/wfsdescribefeaturetype.xml',
                'https://www.dov.vlaanderen.be/geoserver/dov-pub/Sonderingen'
                '/ows?service=wfs&version=1.1.0&request=DescribeFeatureType')

    for xsd_schema in Sondering.get_xsd_schemas():
        update_file(
            'types/sondering/xsd_%s.xml' % xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/informele_stratigrafie

    update_file('types/interpretaties/informele_stratigrafie'
                '/informele_stratigrafie.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/1962'
                '-101692.xml')

    update_file('types/interpretaties/informele_stratigrafie'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':informele_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/1962-101692%27')

    update_file('types/interpretaties/informele_stratigrafie/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':informele_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/1962-101692%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/informele_stratigrafie/fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=b6c651f9-5972-4252-ae10-ad69ad08e78d')

    update_file('types/interpretaties/informele_stratigrafie/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=bd171ea4-2509-478d-a21c-c2728d3a9051')

    update_file(
        'types/interpretaties/informele_stratigrafie/wfsdescribefeaturetype'
        '.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/informele_stratigrafie/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in InformeleStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/informele_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/formele_stratigrafie

    update_file('types/interpretaties/formele_stratigrafie'
                '/formele_stratigrafie.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/2011-'
                '249333.xml')

    update_file('types/interpretaties/formele_stratigrafie'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':formele_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2011-249333%27')

    update_file('types/interpretaties/formele_stratigrafie/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':formele_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2011-249333%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/formele_stratigrafie/fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=68405b5d-51e6-44d0-b634-b580bc2f9eb6')

    update_file('types/interpretaties/formele_stratigrafie/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=212af8cd-bffd-423c-9d2b-69c544ab3b04')

    update_file(
        'types/interpretaties/formele_stratigrafie/wfsdescribefeaturetype'
        '.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/formele_stratigrafie/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in FormeleStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/formele_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/hydrogeologische_stratigrafie

    update_file('types/interpretaties/hydrogeologische_stratigrafie'
                '/hydrogeologische_stratigrafie.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/'
                '2001-186543.xml')

    update_file('types/interpretaties/hydrogeologische_stratigrafie'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':hydrogeologische_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2001-186543%27')

    update_file('types/interpretaties/hydrogeologische_stratigrafie'
                '/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':hydrogeologische_stratigrafie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data/'
                'interpretatie/2001-186543%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie/'
        'fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=b89e72de-35a9-4bca-8d0b-712d1e881ea6')

    update_file('types/interpretaties/hydrogeologische_stratigrafie/'
                'md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=25c5d9fa-c2ba-4184-b796-fde790e73d39')

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie/'
        'wfsdescribefeaturetype.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/hydrogeologische_stratigrafie/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in HydrogeologischeStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/hydrogeologische_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/lithologische_beschrijvingen

    update_file('types/interpretaties/lithologische_beschrijvingen'
                '/lithologische_beschrijvingen.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/1958'
                '-003925.xml')

    update_file('types/interpretaties/lithologische_beschrijvingen'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':lithologische_beschrijvingen&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/1958-003925%27')

    update_file('types/interpretaties/lithologische_beschrijvingen/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':lithologische_beschrijvingen&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/1958-003925%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=2450d592-29bc-4970-a89f-a7b14bd38dc2')

    update_file('types/interpretaties/lithologische_beschrijvingen/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=45b5610e-9a66-42bd-b920-af099e399f3b')

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/wfsdescribefeaturetype'
        '.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/lithologische_beschrijvingen/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in LithologischeBeschrijvingen.get_xsd_schemas():
        update_file(
            'types/interpretaties/lithologische_beschrijvingen/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/gecodeerde_lithologie

    update_file('types/interpretaties/gecodeerde_lithologie'
                '/gecodeerde_lithologie.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/2001'
                '-046845.xml')

    update_file('types/interpretaties/gecodeerde_lithologie'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':gecodeerde_lithologie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2001-046845%27')

    update_file('types/interpretaties/gecodeerde_lithologie/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':gecodeerde_lithologie&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2001-046845%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/gecodeerde_lithologie/fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=0032241d-8920-415e-b1d8-fa0a48154904')

    update_file('types/interpretaties/gecodeerde_lithologie/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=35d630e4-9145-46f9-b7dc-da290a0adc55')

    update_file(
        'types/interpretaties/gecodeerde_lithologie/wfsdescribefeaturetype'
        '.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/gecodeerde_lithologie/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in GecodeerdeLithologie.get_xsd_schemas():
        update_file(
            'types/interpretaties/gecodeerde_lithologie/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/interpretaties/geotechnische_codering

    update_file('types/interpretaties/geotechnische_codering'
                '/geotechnische_codering.xml',
                'https://www.dov.vlaanderen.be/data/interpretatie/2016'
                '-298511.xml')

    update_file('types/interpretaties/geotechnische_codering'
                '/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':geotechnische_coderingen&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2016-298511%27')

    update_file('types/interpretaties/geotechnische_codering/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=interpretaties'
                ':geotechnische_coderingen&maxFeatures=1&CQL_Filter'
                '=Interpretatiefiche=%27https://www.dov.vlaanderen.be/data'
                '/interpretatie/2016-298511%27',
                get_first_featuremember)

    update_file(
        'types/interpretaties/geotechnische_codering/fc_featurecatalogue.xml',
        'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
        '?Service=CSW&Request=GetRecordById&Version=2.0.2'
        '&outputSchema=http://www.isotc211.org/2005/gmd'
        '&elementSetName=full&id=85404aa6-2d88-46f6-ae5a-575aece71efd')

    update_file('types/interpretaties/geotechnische_codering/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=6a3dc5d4-0744-4d9c-85ce-da50913851cc')

    update_file(
        'types/interpretaties/geotechnische_codering/wfsdescribefeaturetype'
        '.xml',
        'https://www.dov.vlaanderen.be/geoserver/interpretaties'
        '/geotechnische_coderingen/ows?service=wfs&version=1.1.0&request'
        '=DescribeFeatureType')

    for xsd_schema in GeotechnischeCodering.get_xsd_schemas():
        update_file(
            'types/interpretaties/geotechnische_codering/xsd_%s.xml' %
            xsd_schema.split('/')[-1],
            xsd_schema)

    # types/grondwaterfilter

    update_file('types/grondwaterfilter/grondwaterfilter.xml',
                'https://www.dov.vlaanderen.be/data/filter/2003-004471.xml')

    update_file('types/grondwaterfilter/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName='
                'gw_meetnetten:meetnetten&maxFeatures=1&'
                'CQL_Filter=filterfiche=%27https://www.dov'
                '.vlaanderen.be/data/filter/2003-004471%27')

    update_file('types/grondwaterfilter/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName='
                'gw_meetnetten:meetnetten&maxFeatures=1&'
                'CQL_Filter=filterfiche=%27https://www.dov'
                '.vlaanderen.be/data/filter/2003-004471%27',
                get_first_featuremember)

    update_file('types/grondwaterfilter/fc_featurecatalogue.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=b142965f-b2aa-429e-86ff-a7cb0e065d48')

    update_file('types/grondwaterfilter/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=6c39d716-aecc-4fbc-bac8-4f05a49a78d5')

    update_file('types/grondwaterfilter/wfsdescribefeaturetype.xml',
                'https://www.dov.vlaanderen.be/geoserver/gw_meetnetten/'
                'meetnetten/ows?service=wfs&version=1.1.0&'
                'request=DescribeFeatureType')

    for xsd_schema in GrondwaterFilter.get_xsd_schemas():
        update_file(
            'types/grondwaterfilter/xsd_%s.xml' % xsd_schema.split('/')[-1],
            xsd_schema)

    # util/owsutil

    update_file('util/owsutil/fc_featurecatalogue_notfound.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=badfc000-0000-0000-0000-badfc00badfc')

    update_file('util/owsutil/wfscapabilities.xml',
                'https://www.dov.vlaanderen.be/geoserver/wfs?request'
                '=getcapabilities&service=wfs&version=1.1.0')
