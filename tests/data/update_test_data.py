"""Script to update the testdata based on DOV webservices."""
from owslib.etree import etree
from owslib.util import openURL


def get_first_featuremember(wfs_response):
    tree = etree.fromstring(wfs_response.encode('utf-8'))

    feature_members = tree.find('.//{http://www.opengis.net/gml}'
                                'featureMembers')

    if feature_members is not None:
        for ft in feature_members:
            return etree.tostring(ft).decode('utf-8')


def update_file(filepath, url, process_fn=None):
    print('Updating %s ...' % filepath)
    try:
        data = openURL(url).read()
        if type(data) is bytes:
            data = data.decode('utf-8')
    except:
        return
    else:
        with open(filepath, 'wb') as f:
            if process_fn:
                data = process_fn(data)
            f.write(data.encode('utf-8'))


if __name__ == '__main__':
    # search

    update_file('search/wfsgetfeature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub:Boringen'
                '&maxFeatures=1&CQL_Filter=fiche=%27https://www.dov'
                '.vlaanderen.be/data/boring/2004-103984%27')

    # types/boring

    update_file('types/boring/boring.xml',
                'https://www.dov.vlaanderen.be/data/boring/2004-103984.xml')

    update_file('types/boring/feature.xml',
                'https://www.dov.vlaanderen.be/geoserver/ows?service=WFS'
                '&version=1.1.0&request=GetFeature&typeName=dov-pub:Boringen'
                '&maxFeatures=1&CQL_Filter=fiche=%27https://www.dov'
                '.vlaanderen.be/data/boring/2004-103984%27',
                get_first_featuremember)

    # util/owsutil

    update_file('util/owsutil/fc_featurecatalogue.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=c0cbd397-520f-4ee1-aca7-d70e271eeed6')

    update_file('util/owsutil/fc_featurecatalogue_notfound.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=badfc000-0000-0000-0000-badfc00badfc')

    update_file('util/owsutil/md_metadata.xml',
                'https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw'
                '?Service=CSW&Request=GetRecordById&Version=2.0.2'
                '&outputSchema=http://www.isotc211.org/2005/gmd'
                '&elementSetName=full&id=4e20bf9c-3a5c-42be-b5b6-bef6214d1fa7')

    update_file('util/owsutil/wfscapabilities.xml',
                'https://www.dov.vlaanderen.be/geoserver/wfs?request'
                '=getcapabilities&service=wfs&version=1.1.0')

    update_file('util/owsutil/wfsdescribefeaturetype.xml',
                'https://www.dov.vlaanderen.be/geoserver/dov-pub/Boringen'
                '/ows?service=wfs&version=1.1.0&request=DescribeFeatureType')
