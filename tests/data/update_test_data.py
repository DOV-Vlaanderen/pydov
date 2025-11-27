"""Script to update the testdata based on DOV webservices."""
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from owslib.etree import etree

from pydov.types.bodemlocatie import Bodemlocatie
from pydov.types.bodemdiepteinterval import Bodemdiepteinterval
from pydov.types.bodemobservatie import Bodemobservatie
from pydov.types.bodemsite import Bodemsite
from pydov.types.bodemclassificatie import Bodemclassificatie
from pydov.types.boring import Boring
from pydov.types.monster import Monster
from pydov.types.observatie import Observatie
from pydov.types.grondwaterfilter import GrondwaterFilter
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
from pydov.util.codelists import AbstractResolvableCodeList

from tests.abstract import ServiceCheck


def get_first_featuremember(wfs_response):
    tree = etree.fromstring(wfs_response.encode('utf-8'))

    first_feature_member = tree.find(
        './/{http://www.opengis.net/wfs/2.0}member')

    if first_feature_member is not None:
        return etree.tostring(first_feature_member[0]).decode('utf-8')


def update_file_raw(filepath, data, session=None):
    output = 'Updating {} ... '.format(filepath)
    failed = False
    filepath = os.path.join(os.path.dirname(__file__), filepath)

    if isinstance(data, bytes):
        data = data.decode('utf-8')

    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    with open(filepath, 'wb') as f:
        f.write(data.encode('utf-8'))
        output += ' OK.\n'

    return output, failed


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

    def update_file_fn(filepath, fn):
        pool.execute(update_file_raw, (filepath, fn()))

    def get_codelists(cls, path):

        def update_codelist_file(codelist):
            id = codelist.get_id()
            update_file_fn(
                '{}/codelist_{}'.format(path, id),
                codelist.get_remote_codelist)

        for codelist in cls.get_codelists(AbstractResolvableCodeList):
            update_codelist_file(codelist)

        for fieldset in cls.get_fieldsets().values():
            for codelist in \
                    fieldset['class'].get_codelists(AbstractResolvableCodeList):
                update_codelist_file(codelist)

        for subtype in cls.get_subtypes().values():
            for codelist in \
                    subtype['class'].get_codelists(AbstractResolvableCodeList):
                update_codelist_file(codelist)

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

    get_codelists(Boring, 'types/boring')

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

    get_codelists(Sondering, 'types/sondering')

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

    get_codelists(InformeleStratigrafie,
                  'types/interpretaties/informele_stratigrafie')

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

    get_codelists(FormeleStratigrafie,
                  'types/interpretaties/formele_stratigrafie')

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

    get_codelists(HydrogeologischeStratigrafie,
                  'types/interpretaties/hydrogeologische_stratigrafie')

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

    get_codelists(LithologischeBeschrijvingen,
                  'types/interpretaties/lithologische_beschrijvingen')

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

    get_codelists(GecodeerdeLithologie,
                  'types/interpretaties/gecodeerde_lithologie')

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

    get_codelists(GeotechnischeCodering,
                  'types/interpretaties/geotechnische_codering')

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

    get_codelists(
        InformeleHydrogeologischeStratigrafie,
        'types/interpretaties/informele_hydrogeologische_stratigrafie')

    # types/grondwaterfilter

    update_file('types/grondwaterfilter/grondwaterfilter.xml',
                build_dov_url('data/filter/1997-000494.xml'))

    update_file('types/grondwaterfilter/wfsgetfeature.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/1997-000494%27')))

    update_file('types/grondwaterfilter/feature.xml',
                build_dov_url('geoserver/ows?service=WFS'
                              '&version=2.0.0&request=GetFeature&typeName='
                              'gw_meetnetten:meetnetten&count=1&'
                              'CQL_Filter=filterfiche=%27' + build_dov_url(
                                  'data/filter/1997-000494%27')),
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

    get_codelists(GrondwaterFilter, 'types/grondwaterfilter')

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

    get_codelists(QuartairStratigrafie,
                  'types/interpretaties/quartaire_stratigrafie')

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

    get_codelists(Bodemlocatie, 'types/bodemlocatie')

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

    get_codelists(Bodemdiepteinterval, 'types/bodemdiepteinterval')

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

    get_codelists(Bodemobservatie, 'types/bodemobservatie')

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

    get_codelists(Bodemsite, 'types/bodemsite')

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

    get_codelists(Bodemclassificatie, 'types/bodemclassificatie')

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

    get_codelists(GrondwaterVergunning, 'types/grondwatervergunning')

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

    # types/monster

    update_file('types/monster/monster.xml',
                build_dov_url('data/monster/2022-324453.xml'))

    update_file(
        'types/monster/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'monster:monsters&maxFeatures=1&CQL_Filter'
            '=permkey_monster=%272022-324453%27'))

    update_file(
        'types/monster/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS'
            '&version=2.0.0&request=GetFeature&typeName='
            'monster:monsters&maxFeatures=1&CQL_Filter'
            '=permkey_monster=%272022-324453%27'),
        get_first_featuremember)

    update_file(
        'types/monster/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=d0770640-32b9-44a2-8784-32daa1d91fc5'))

    update_file(
        'types/monster/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&'
            'id=afd479f5-4f6a-41cf-9604-9993e54b1544'))

    update_file(
        'types/monster/wfsdescribefeaturetype'
        '.xml',
        build_dov_url('geoserver/monster'
                      '/monsters/ows?service=wfs&version=2.0.0&request'
                      '=DescribeFeatureType'))

    get_codelists(Monster, 'types/monster')

    # types/observatie

    update_file('types/observatie/observatie.xml',
                build_dov_url('data/observatie/2022-11963810.xml'))

    update_file(
        'types/observatie/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2022-11963810%27'))
    )

    update_file(
        'types/observatie/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2022-11963810%27')),
        get_first_featuremember)

    update_file(
        'types/observatie/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=0ee52b15-12a5-4314-a8af-0b37ee8bf766'))

    update_file(
        'types/observatie/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=7e166b29-f24b-494b-af66-acc82deb5af2'))

    update_file(
        'types/observatie/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/monster/wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typeName=monster:observaties'))

    get_codelists(Observatie, 'types/observatie')

    # types/observatie_fractiemetingen

    update_file('types/observatie_fractiemeting/observatie.xml',
                build_dov_url('data/observatie/1995-10282748.xml'))

    update_file(
        'types/observatie_fractiemeting/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/1995-10282748%27'))
    )

    update_file(
        'types/observatie_fractiemeting/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/1995-10282748%27')),
        get_first_featuremember)

    update_file(
        'types/observatie_fractiemeting/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=0ee52b15-12a5-4314-a8af-0b37ee8bf766'))

    update_file(
        'types/observatie_fractiemeting/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=7e166b29-f24b-494b-af66-acc82deb5af2'))

    update_file(
        'types/observatie_fractiemeting/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/monster/wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typeName=monster:observaties'))

    get_codelists(Observatie, 'types/observatie_fractiemeting')

    # types/observatie_meetreeks

    update_file('types/observatie_meetreeks/observatie.xml',
                build_dov_url('data/observatie/2025-43568400.xml'))

    update_file(
        'types/observatie_meetreeks/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2025-43568400%27'))
    )

    update_file(
        'types/observatie_meetreeks/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2025-43568400%27')),
        get_first_featuremember)

    update_file(
        'types/observatie_meetreeks/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=0ee52b15-12a5-4314-a8af-0b37ee8bf766'))

    update_file(
        'types/observatie_meetreeks/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=7e166b29-f24b-494b-af66-acc82deb5af2'))

    update_file(
        'types/observatie_meetreeks/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/monster/wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typeName=monster:observaties'))

    get_codelists(Observatie, 'types/observatie_meetreeks')

    # types/observatie_secundaire_parameter

    update_file('types/observatie_secundaire_parameter/observatie.xml',
                build_dov_url('data/observatie/2019-000555.xml'))

    update_file(
        'types/observatie_secundaire_parameter/wfsgetfeature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2019-000555%27'))
    )

    update_file(
        'types/observatie_secundaire_parameter/feature.xml',
        build_dov_url(
            'geoserver/ows?service=WFS&version=2.0.0&request=GetFeature'
            '&typeName=monster:observaties&count=1&CQL_Filter=observatie_link=%27' + build_dov_url(
                'data/observatie/2019-000555%27')),
        get_first_featuremember)

    update_file(
        'types/observatie_secundaire_parameter/fc_featurecatalogue.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gfc'
            '&elementSetName=full&id=0ee52b15-12a5-4314-a8af-0b37ee8bf766'))

    update_file(
        'types/observatie_secundaire_parameter/md_metadata.xml',
        build_dov_url(
            'geonetwork/srv/dut/csw'
            '?Service=CSW&Request=GetRecordById&Version=2.0.2'
            '&outputSchema=http://www.isotc211.org/2005/gmd'
            '&elementSetName=full&id=7e166b29-f24b-494b-af66-acc82deb5af2'))

    update_file(
        'types/observatie_secundaire_parameter/wfsdescribefeaturetype.xml',
        build_dov_url(
            'geoserver/monster/wfs?service=WFS&version=2.0.0&request=DescribeFeatureType&typeName=monster:observaties'))

    get_codelists(Observatie, 'types/observatie_secundaire_parameter')

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
