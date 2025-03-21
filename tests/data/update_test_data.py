"""Script to update the testdata based on DOV webservices."""
import os
import sys

from owslib.etree import etree
import requests
import pydov

from pydov.types.bodemlocatie import Bodemlocatie
from pydov.types.bodemdiepteinterval import Bodemdiepteinterval
from pydov.types.bodemmonster import Bodemmonster
from pydov.types.bodemobservatie import Bodemobservatie
from pydov.types.bodemsite import Bodemsite
from pydov.types.bodemclassificatie import Bodemclassificatie
from pydov.types.boring import Boring
from pydov.types.grondmonster import Grondmonster
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.types.grondwatermonster import GrondwaterMonster
from pydov.types.grondwatervergunning import GrondwaterVergunning
from pydov.types.interpretaties import (FormeleStratigrafie,
                                        GecodeerdeLithologie,
                                        GeotechnischeCodering,
                                        HydrogeologischeStratigrafie,
                                        InformeleHydrogeologischeStratigrafie,
                                        InformeleStratigrafie,
                                        LithologischeBeschrijvingen,
                                        QuartairStratigrafie)
from pydov.types.sondering import Sondering
from pydov.util.dovutil import build_dov_url, get_remote_url
from pydov.util.net import LocalSessionThreadPool
from tests.abstract import ServiceCheck


def get_first_featuremember(wfs_response):
    tree = etree.fromstring(wfs_response.encode('utf-8'))

    first_feature_member = tree.find(
        './/{http://www.opengis.net/wfs/2.0}member')

    if first_feature_member is not None:
        return etree.tostring(first_feature_member[0]).decode('utf-8')


def update_file_real(filepath, url, process_fn=None, session=None):
    output = 'Updating {} ... '.format(filepath)
    failed = False
    filepath = os.path.join(os.path.dirname(__file__), filepath)
    try:
        data = get_remote_url(url, session)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
    except Exception as e:
        output += ' FAILED:\n   {}.\n'.format(e)
        failed = True
    else:
        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        with open(filepath, 'wb') as f:
            if process_fn:
                try:
                    data = process_fn(data)
                except Exception as e:
                    output += ' FAILED:\n   {}.\n'.format(e)
                    failed = True
                else:
                    if data is not None:
                        f.write(data.encode('utf-8'))
                    else:
                        output += ' FAILED:\n   {}.\n'.format(
                            'No data returned by process function')
                        failed = True
            else:
                f.write(data.encode('utf-8'))
                output += ' OK.\n'

    return output, failed


if __name__ == '__main__':
    if not ServiceCheck.service_ok():
        print('Not updating test data as services are unavailable.')
        sys.exit(1)

    pool = LocalSessionThreadPool()

    def update_file(filepath, url, process_fn=None):
        pool.execute(update_file_real, (filepath, url, process_fn))

    # types/boring
    update_file('types/boring/boring.xml',
                build_dov_url('data/boring/2004-103984.xml'))

    update_file(
        'types/boring/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=dov-pub:Boringen'
            '&count=1&CQL_Filter=fiche=%27' +
            build_dov_url('data/boring/2004-103984%27')))

    update_file(
        'types/boring/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=dov-pub:Boringen'
            '&count=1&CQL_Filter=fiche=%27' +
            build_dov_url('data/boring/2004-103984%27')),
        get_first_featuremember)

    update_file(
        'types/boring/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=c0cbd397-520f-4ee1-aca7'
            '-d70e271eeed6'))

    update_file(
        'types/boring/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=4e20bf9c-3a5c-42be-b5b6'
            '-bef6214d1fa7'))

    update_file(
        'types/boring/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/dov-pub/Boringen'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Boring.get_xsd_schemas():
        update_file(
            'types/boring/xsd_{}.xml'.format(xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/sondering

    update_file('types/sondering/sondering.xml',
                build_dov_url('data/sondering/2002-018435.xml'))

    update_file(
        'types/sondering/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=dov-pub'
            ':Sonderingen&count=1&CQL_Filter=fiche=%27' +
            build_dov_url('data/sondering/2002-018435%27')))

    update_file(
        'types/sondering/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=dov-pub'
            ':Sonderingen&count=1&CQL_Filter=fiche=%27' +
            build_dov_url('data/sondering/2002-018435%27')),
        get_first_featuremember)

    update_file(
        'types/sondering/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=bd539ba5-5f4d-4c43-9662'
            '-51c16caea351'))

    update_file(
        'types/sondering/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=b397faec-1b64-4854-8000'
            '-2375edb3b1a8'))

    update_file(
        'types/sondering/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/dov-pub/Sonderingen'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Sondering.get_xsd_schemas():
        update_file(
            'types/sondering/xsd_{}.xml'.format(xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/interpretaties/informele_stratigrafie

    update_file('types/interpretaties/informele_stratigrafie'
                '/informele_stratigrafie.xml',
                build_dov_url('data/interpretatie/1962-101692.xml'))

    update_file(
        'types/interpretaties/informele_stratigrafie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':informele_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1962-101692%27'))

    update_file(
        'types/interpretaties/informele_stratigrafie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':informele_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1962-101692%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/informele_stratigrafie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=b6c651f9-5972-4252-ae10-ad69ad08e78d'))

    update_file(
        'types/interpretaties/informele_stratigrafie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=bd171ea4-2509-478d-a21c'
            '-c2728d3a9051'))

    update_file(
        'types/interpretaties/informele_stratigrafie/wfsdescribefeaturetype'
        '.xml', build_dov_url(
            'geoserver/interpretaties'
            '/informele_stratigrafie/ows?service=wfs&version=2.0.0&request'
            '=DescribeFeatureType'))

    for xsd_schema in InformeleStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/informele_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/formele_stratigrafie

    update_file('types/interpretaties/formele_stratigrafie'
                '/formele_stratigrafie.xml',
                build_dov_url('data/interpretatie/2011-249333.xml'))

    update_file(
        'types/interpretaties/formele_stratigrafie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':formele_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2011-249333%27'))

    update_file(
        'types/interpretaties/formele_stratigrafie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':formele_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2011-249333%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/formele_stratigrafie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=68405b5d-51e6-44d0-b634-b580bc2f9eb6'))

    update_file(
        'types/interpretaties/formele_stratigrafie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=212af8cd-bffd-423c-9d2b'
            '-69c544ab3b04'))

    update_file(
        'types/interpretaties/formele_stratigrafie/wfsdescribefeaturetype'
        '.xml', build_dov_url(
            'geoserver/interpretaties'
            '/formele_stratigrafie/ows?service=wfs&version=2.0.0&request'
            '=DescribeFeatureType'))

    for xsd_schema in FormeleStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/formele_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/hydrogeologische_stratigrafie

    update_file('types/interpretaties/hydrogeologische_stratigrafie'
                '/hydrogeologische_stratigrafie.xml',
                build_dov_url('data/interpretatie/2001-186543.xml'))

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':hydrogeologische_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2001-186543%27'))

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie'
        '/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':hydrogeologische_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data/'
            'interpretatie/2001-186543%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie/'
        'fc_featurecatalogue.xml', build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=b89e72de-35a9-4bca-8d0b-712d1e881ea6'))

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie/'
        'md_metadata.xml', build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=25c5d9fa-c2ba-4184-b796'
            '-fde790e73d39'))

    update_file(
        'types/interpretaties/hydrogeologische_stratigrafie/'
        'wfsdescribefeaturetype.xml', build_dov_url(
            'geoserver/interpretaties'
            '/hydrogeologische_stratigrafie/ows?service=wfs&version=2.0.0'
            '&request=DescribeFeatureType'))

    for xsd_schema in HydrogeologischeStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/hydrogeologische_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/lithologische_beschrijvingen

    update_file('types/interpretaties/lithologische_beschrijvingen'
                '/lithologische_beschrijvingen.xml',
                build_dov_url('data/interpretatie/1958-003925.xml'))

    update_file(
        'types/interpretaties/lithologische_beschrijvingen'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':lithologische_beschrijvingen&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1958-003925%27'))

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':lithologische_beschrijvingen&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1958-003925%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/'
        'fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=2450d592-29bc-4970-a89f-a7b14bd38dc2'))

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=45b5610e-9a66-42bd-b920'
            '-af099e399f3b'))

    update_file(
        'types/interpretaties/lithologische_beschrijvingen/'
        'wfsdescribefeaturetype.xml', build_dov_url(
            'geoserver/interpretaties'
            '/lithologische_beschrijvingen/ows?service=wfs&version=2.0.0'
            '&request=DescribeFeatureType'))

    for xsd_schema in LithologischeBeschrijvingen.get_xsd_schemas():
        update_file(
            'types/interpretaties/lithologische_beschrijvingen/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/gecodeerde_lithologie

    update_file('types/interpretaties/gecodeerde_lithologie'
                '/gecodeerde_lithologie.xml',
                build_dov_url('data/interpretatie/2001-046845.xml'))

    update_file(
        'types/interpretaties/gecodeerde_lithologie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':gecodeerde_lithologie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2001-046845%27'))

    update_file(
        'types/interpretaties/gecodeerde_lithologie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':gecodeerde_lithologie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2001-046845%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/gecodeerde_lithologie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=0032241d-8920-415e-b1d8-fa0a48154904'))

    update_file(
        'types/interpretaties/gecodeerde_lithologie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=35d630e4-9145-46f9-b7dc'
            '-da290a0adc55'))

    update_file(
        'types/interpretaties/gecodeerde_lithologie/wfsdescribefeaturetype'
        '.xml', build_dov_url(
            'geoserver/interpretaties'
            '/gecodeerde_lithologie/ows?service=wfs&version=2.0.0&request'
            '=DescribeFeatureType'))

    for xsd_schema in GecodeerdeLithologie.get_xsd_schemas():
        update_file(
            'types/interpretaties/gecodeerde_lithologie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/geotechnische_codering

    update_file('types/interpretaties/geotechnische_codering'
                '/geotechnische_codering.xml',
                build_dov_url('data/interpretatie/2016-298511.xml'))

    update_file(
        'types/interpretaties/geotechnische_codering'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':geotechnische_coderingen&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2016-298511%27'))

    update_file(
        'types/interpretaties/geotechnische_codering/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':geotechnische_coderingen&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2016-298511%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/geotechnische_codering/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=85404aa6-2d88-46f6-ae5a-575aece71efd'))

    update_file(
        'types/interpretaties/geotechnische_codering/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=6a3dc5d4-0744-4d9c-85ce'
            '-da50913851cc'))

    update_file(
        'types/interpretaties/geotechnische_codering/wfsdescribefeaturetype'
        '.xml', build_dov_url(
            'geoserver/interpretaties'
            '/geotechnische_coderingen/ows?service=wfs&version=2.0.0&request'
            '=DescribeFeatureType'))

    for xsd_schema in GeotechnischeCodering.get_xsd_schemas():
        update_file(
            'types/interpretaties/geotechnische_codering/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/interpretaties/informele_hydrogeologische_stratigrafie

    update_file('types/interpretaties/informele_hydrogeologische_stratigrafie'
                '/informele_hydrogeologische_stratigrafie.xml',
                build_dov_url('data/interpretatie/2003-297774.xml'))

    update_file(
        'types/interpretaties/informele_hydrogeologische_stratigrafie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':informele_hydrogeologische_stratigrafie&count=1'
            '&CQL_Filter=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2003-297774%27'))

    update_file(
        'types/interpretaties/informele_hydrogeologische_stratigrafie'
        '/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':informele_hydrogeologische_stratigrafie&count=1'
            '&CQL_Filter=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/2003-297774%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/informele_hydrogeologische_stratigrafie'
        '/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=69f71840-bd29-4b59-9b02-4e36aafaa041'))

    update_file(
        'types/interpretaties/informele_hydrogeologische_stratigrafie'
        '/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full'
            '&id=ca1d704a-cdee-4968-aa65-9c353863e4b1'))

    update_file(
        'types/interpretaties/informele_hydrogeologische_stratigrafie/'
        'wfsdescribefeaturetype.xml', build_dov_url(
            'geoserver/interpretaties'
            '/informele_hydrogeologische_stratigrafie/'
            'ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in InformeleHydrogeologischeStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/informele_hydrogeologische_stratigrafie/'
            'xsd_%s.xml' % xsd_schema.split('/')[-1], xsd_schema)

    # types/grondwaterfilter

    update_file('types/grondwaterfilter/grondwaterfilter.xml',
                build_dov_url('data/filter/2003-004471.xml'))

    update_file('types/grondwaterfilter/wfsgetfeature.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/2003-004471%27')))

    update_file('types/grondwaterfilter/feature.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/2003-004471%27')),
                get_first_featuremember)

    update_file(
        'types/grondwaterfilter/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=b142965f-b2aa-429e-86ff'
            '-a7cb0e065d48'))

    update_file(
        'types/grondwaterfilter/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=6c39d716-aecc-4fbc-bac8'
            '-4f05a49a78d5'))

    update_file('types/grondwaterfilter/wfsdescribefeaturetype.xml',
                build_dov_url('geoserver/gw_meetnetten/'
                              'meetnetten/ows?service=wfs&version=2.0.0&'
                              'request=DescribeFeatureType'))

    for xsd_schema in GrondwaterFilter.get_xsd_schemas():
        update_file(
            'types/grondwaterfilter/xsd_%s.xml' % xsd_schema.split('/')[-1],
            xsd_schema)

    update_file('types/grondwaterfilter/grondwaterfilter_geenpeilmeting.xml',
                build_dov_url('data/filter/1976-101132.xml'))

    update_file('types/grondwaterfilter/wfsgetfeature_geenpeilmeting.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/1976-101132%27')))

    update_file('types/grondwaterfilter/feature_geenpeilmeting.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/1976-101132%27')),
                get_first_featuremember)

    # types/grondwatermonster

    update_file('types/grondwatermonster/grondwatermonster.xml',
                build_dov_url('data/watermonster/2006-115684.xml'))

    update_file(
        'types/grondwatermonster/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'gw_meetnetten:grondwatermonsters&count=1&'
            'CQL_Filter=grondwatermonsterfiche=%27' +
            build_dov_url('data/watermonster/2006-115684') +
            '%27'))

    update_file(
        'types/grondwatermonster/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'gw_meetnetten:grondwatermonsters&count=1&'
            'CQL_Filter=grondwatermonsterfiche=%27' +
            build_dov_url('data/watermonster/2006-115684') +
            '%27'),
        get_first_featuremember)

    update_file(
        'types/grondwatermonster/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&'
            'id=639c9612-4bbb-4826-86fd-fec9afd49bf7'))

    update_file(
        'types/grondwatermonster/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&'
            'id=0b378716-39fb-4151-96c5-2021672f4762'))

    update_file(
        'types/grondwatermonster/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/gw_meetnetten/'
            'grondwatermonsters/ows?service=wfs&version=2.0.0&'
            'request=DescribeFeatureType'))

    for xsd_schema in GrondwaterMonster.get_xsd_schemas():
        update_file(
            'types/grondwatermonster/xsd_%s.xml' % xsd_schema.split('/')[-1],
            xsd_schema)

    # util/owsutil

    update_file(
        'util/owsutil/fc_featurecatalogue_notfound.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=badfc000-0000-0000-0000'
            '-badfc00badfc'))

    update_file('util/owsutil/wfscapabilities.xml',
                build_dov_url('geoserver/wfs?request'
                              '=getcapabilities&service=wfs&version=2.0.0'))

    # types/interpretaties/quartaire_stratigrafie

    update_file('types/interpretaties/quartaire_stratigrafie'
                '/quartaire_stratigrafie.xml',
                build_dov_url('data/interpretatie/1999-057087.xml'))

    update_file(
        'types/interpretaties/quartaire_stratigrafie'
        '/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':quartaire_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1999-057087%27'))

    update_file(
        'types/interpretaties/quartaire_stratigrafie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=interpretaties'
            ':quartaire_stratigrafie&count=1&CQL_Filter'
            '=Interpretatiefiche=%27') +
        build_dov_url(
            'data'
            '/interpretatie/1999-057087%27'),
        get_first_featuremember)

    update_file(
        'types/interpretaties/quartaire_stratigrafie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=d40ef884-3278-45db-ad69-2c2a8c3981c3'))

    update_file(
        'types/interpretaties/quartaire_stratigrafie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=8b204ed6-e44c-4567-bbe8'
            '-bd427eba082c'))

    update_file(
        'types/interpretaties/quartaire_stratigrafie/wfsdescribefeaturetype'
        '.xml', build_dov_url(
            'geoserver/interpretaties'
            '/quartaire_stratigrafie/ows?service=wfs&version=2.0.0&request'
            '=DescribeFeatureType'))

    for xsd_schema in QuartairStratigrafie.get_xsd_schemas():
        update_file(
            'types/interpretaties/quartaire_stratigrafie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/grondmonster

    update_file('types/grondmonster/grondmonster.xml',
                build_dov_url('data/grondmonster/2018-211728.xml'))

    update_file(
        'types/grondmonster/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'boringen:grondmonsters&count=1&CQL_Filter'
            '=monster_link=%27' +
            build_dov_url(
                'data'
                '/monster/2018-211728') +
            '%27'))

    update_file(
        'types/grondmonster/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'boringen:grondmonsters&count=1&CQL_Filter'
            '=monster_link=%27' +
            build_dov_url(
                'data'
                '/monster/2018-211728') +
            '%27'),
        get_first_featuremember)

    update_file(
        'types/grondmonster/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=b9338fb5-fc9c-4229-858b-06a5fa3ee49d'))

    update_file(
        'types/grondmonster/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&'
            'id=6edeab46-2cfc-4aa2-ae03-307d772f34ae'))

    update_file(
        'types/grondmonster/wfsdescribefeaturetype'
        '.xml',
        build_dov_url('geoserver/boringen'
                      '/grondmonsters/ows?service=wfs&version=2.0.0&request'
                      '=DescribeFeatureType'))

    for xsd_schema in Grondmonster.get_xsd_schemas():
        update_file(
            'types/grondmonster/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/bodemlocatie
    update_file('types/bodemlocatie/bodemlocatie.xml',
                build_dov_url('data/bodemlocatie/2011-000002.xml'))

    update_file(
        'types/bodemlocatie/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemlocaties'
            '&count=1&CQL_Filter=Bodemlocatiefiche=%27' +
            build_dov_url('data/bodemlocatie/2011-000002%27')))

    update_file(
        'types/bodemlocatie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemlocaties'
            '&count=1&CQL_Filter=Bodemlocatiefiche=%27' +
            build_dov_url('data/bodemlocatie/2011-000002%27')),
        get_first_featuremember)

    update_file(
        'types/bodemlocatie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=89d4f9a1-0474-4ade-b30f-442c31d17dc6'))

    update_file(
        'types/bodemlocatie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=3f507fd9-24c0-40ab-9328-29f0dff571fe'))

    update_file(
        'types/bodemlocatie/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/bodem/bodemlocaties'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Bodemlocatie.get_xsd_schemas():
        update_file(
            'types/bodemlocatie/xsd_{}.xml'.format(xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/bodemdiepteinterval
    update_file(
        'types/bodemdiepteinterval/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'bodem:bodemdiepteintervallen&count=1&'
            'CQL_Filter=Diepteintervalfiche=%27' +
            build_dov_url('data/bodemdiepteinterval/2018-000004%27')))

    update_file(
        'types/bodemdiepteinterval/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'bodem:bodemdiepteintervallen&count=1&'
            'CQL_Filter=Diepteintervalfiche=%27' +
            build_dov_url('data/bodemdiepteinterval/2018-000004%27')),
        get_first_featuremember)

    update_file(
        'types/bodemdiepteinterval/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=859ad05d-d6fc-4850-b040-1bdac3641ff5'))

    update_file(
        'types/bodemdiepteinterval/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=96a1127f-d7d0-4a33-b24c-04d982b63dce'))

    update_file(
        'types/bodemdiepteinterval/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/bodem/bodemdiepteintervallen'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Bodemdiepteinterval.get_xsd_schemas():
        update_file(
            'types/bodemdiepteinterval/xsd_{}.xml'.format(
                xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/bodemobservatie
    update_file('types/bodemobservatie/bodemobservatie.xml',
                build_dov_url('data/bodemobservatie/2019-001221.xml'))

    update_file(
        'types/bodemobservatie/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemobservaties'
            '&count=1&CQL_Filter=Bodemobservatiefiche=%27' +
            build_dov_url('data/bodemobservatie/2019-001221%27')))

    update_file(
        'types/bodemobservatie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemobservaties'
            '&count=1&CQL_Filter=Bodemobservatiefiche=%27' +
            build_dov_url('data/bodemobservatie/2019-001221%27')),
        get_first_featuremember)

    update_file(
        'types/bodemobservatie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=44df1272-6b57-471b-9f7a-2dc82f760137'))

    update_file(
        'types/bodemobservatie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=dd327fef-62c7-4980-9788-9fac047a1553'))

    update_file(
        'types/bodemobservatie/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/bodem/bodemobservaties'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Bodemobservatie.get_xsd_schemas():
        update_file(
            'types/bodemobservatie/xsd_{}.xml'.format(
                xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/bodemmonster
    update_file('types/bodemmonster/bodemmonster.xml',
                build_dov_url('data/bodemmonster/2015-211807.xml'))

    update_file(
        'types/bodemmonster/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemmonsters'
            '&count=1&CQL_Filter=Bodemmonsterfiche=%27' +
            build_dov_url('data/bodemmonster/2015-211807%27')))

    update_file(
        'types/bodemmonster/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemmonsters'
            '&count=1&CQL_Filter=Bodemmonsterfiche=%27' +
            build_dov_url('data/bodemmonster/2015-211807%27')),
        get_first_featuremember)

    update_file(
        'types/bodemmonster/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=7d69c092-fa5a-4399-86ed-003877f5899e'))

    update_file(
        'types/bodemmonster/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=ff1902b2-7ba2-46be-ba8c-bfcf893444c2'))

    update_file(
        'types/bodemmonster/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/bodem/bodemmonsters'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Bodemmonster.get_xsd_schemas():
        update_file(
            'types/bodemmonster/xsd_{}.xml'.format(xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/bodemsite
    update_file('types/bodemsite/bodemsite.xml',
                build_dov_url('data/bodemsite/2013-000180.xml'))

    update_file(
        'types/bodemsite/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemsites'
            '&count=1&CQL_Filter=Bodemsitefiche=%27' +
            build_dov_url('data/bodemsite/2013-000180%27')))

    update_file(
        'types/bodemsite/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName=bodem:bodemsites'
            '&count=1&CQL_Filter=Bodemsitefiche=%27' +
            build_dov_url('data/bodemsite/2013-000180%27')),
        get_first_featuremember)

    update_file(
        'types/bodemsite/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=955d4bc8-9d78-4af6-9782-85698caae0aa'))

    update_file(
        'types/bodemsite/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=27142078-f0d0-46e3-b97e-2ffc2c6bdd41'))

    update_file(
        'types/bodemsite/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/bodem/bodemsites'
            '/ows?service=wfs&version=2.0.0&request=DescribeFeatureType'))

    for xsd_schema in Bodemsite.get_xsd_schemas():
        update_file(
            'types/bodemsite/xsd_{}.xml'.format(xsd_schema.split('/')[-1]),
            xsd_schema)

    # types/bodemclassificatie
    update_file(
        'types/bodemclassificatie/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'bodem:bodemclassificaties&count=1&'
            'CQL_Filter=Bodemclassificatiefiche=%27' +
            build_dov_url('data/belgischebodemclassificatie/2018-000146%27')))

    update_file(
        'types/bodemclassificatie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'bodem:bodemclassificaties&count=1&'
            'CQL_Filter=Bodemclassificatiefiche=%27' +
            build_dov_url('data/belgischebodemclassificatie/2018-000146%27')),
        get_first_featuremember)

    update_file(
        'types/bodemclassificatie/fc_featurecatalogue.xml',
        build_dov_url('geonetwork/srv/dut/csw'
                      '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                      '&outputSchema=http://www.isotc211.org/2005/gfc'
                      '&elementSetName=full&'
                      'id=9ace8d74-8daa-461f-86bb-273573bc7fa9'))

    update_file('types/bodemclassificatie/md_metadata.xml',
                build_dov_url(
                    'geonetwork/srv/dut/csw'
                    '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                    '&outputSchema=http://www.isotc211.org/2005/gmd'
                    '&elementSetName=full&'
                    'id=7f668812-edc3-464b-870c-08e964f884b6'))

    update_file('types/bodemclassificatie/wfsdescribefeaturetype.xml',
                build_dov_url(
                    'geoserver/bodem/bodemclassificaties'
                    '/ows?service=wfs&version=2.0.0'
                    '&request=DescribeFeatureType'))

    for xsd_schema in Bodemclassificatie.get_xsd_schemas():
        update_file(
            'types/bodemclassificatie/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/gw_vergunningen
    update_file(
        'types/grondwatervergunning/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'gw_vergunningen:alle_verg&count=1&CQL_Filter'
            '=id=38598'))

    update_file(
        'types/grondwatervergunning/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'gw_vergunningen:alle_verg&count=1&CQL_Filter'
            '=id=38598'), get_first_featuremember)

    update_file(
        'types/grondwatervergunning/fc_featurecatalogue.xml',
        build_dov_url('geonetwork/srv/dut/csw'
                      '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                      '&outputSchema=http://www.isotc211.org/2005/gfc'
                      '&elementSetName=full&id=5e605651-'
                      '6b2e-406f-863f-d2eda4d3e534'))

    update_file('types/grondwatervergunning/md_metadata.xml',
                build_dov_url(
                    'geonetwork/srv/dut/csw'
                    '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                    '&outputSchema=http://www.isotc211.org/2005/gmd'
                    '&elementSetName=full&id=1b8d9dce-40b2-450c-81ed-'
                    'decb453b3143'))

    update_file('types/grondwatervergunning/wfsdescribefeaturetype.xml',
                build_dov_url(
                    'geoserver/gw_vergunningen/alle_verg'
                    '/ows?service=wfs&version=2.0.0'
                    '&request=DescribeFeatureType'))

    for xsd_schema in GrondwaterVergunning.get_xsd_schemas():
        update_file(
            'types/grondwatervergunning/xsd_%s.xml' %
            xsd_schema.split('/')[-1], xsd_schema)

    # types/generic

    update_file(
        'types/generic/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'dov-pub:Opdrachten&count=1&CQL_Filter'
            '=fiche=%27' +
            build_dov_url('data/opdracht/2021-026141%27')))

    update_file(
        'types/generic/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'dov-pub:Opdrachten&count=1&CQL_Filter'
            '=fiche=%27' +
            build_dov_url('data/opdracht/2021-026141%27')),
        get_first_featuremember)

    update_file(
        'types/generic/fc_featurecatalogue.xml',
        build_dov_url('geonetwork/srv/dut/csw'
                      '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                      '&outputSchema=http://www.isotc211.org/2005/gfc'
                      '&elementSetName=full&id=f8178f8a-e5a4-4a10-ba31-'
                      '49c4adbc21c2'))

    update_file('types/generic/md_metadata.xml',
                build_dov_url(
                    'geonetwork/srv/dut/csw'
                    '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                    '&outputSchema=http://www.isotc211.org/2005/gmd'
                    '&elementSetName=full&id=8a07f330-3900-4086-89c0-'
                    'cebf940156e5'))

    update_file('types/generic/wfsdescribefeaturetype.xml',
                build_dov_url(
                    'geoserver/dov-pub/Opdrachten'
                    '/ows?service=wfs&version=2.0.0'
                    '&request=DescribeFeatureType'))

    for r in pool.join():
        if r.get_error() is not None:
            sys.stdout.write('{}: {}\n'.format(
                type(r.get_error()).__name__, r.get_error()))
            sys.exit(1)
        else:
            output, failed = r.get_result()
            sys.stdout.write(output)
            if failed:
                sys.exit(1)
