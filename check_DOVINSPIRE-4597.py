import sys
from pydov.util.net import SessionFactory
from owslib.wfs import WebFeatureService
import requests
import time

environments = [
    'on',
    'oe',
    'pr'
]

layers = [
    'bodem:bodemclassificaties',
    'bodem:bodemdiepteintervallen',
    'bodem:bodemlocaties',
    'bodem:bodemmonsters',
    'bodem:bodemobservaties',
    'bodem:bodemsites',
    'boringen:grondmonsters',
    'dov-pub:Boringen',
    'dov-pub:Sonderingen',
    'gw_meetnetten:grondwatermonsters',
    'gw_meetnetten:meetnetten',
    'gw_vergunningen:alle_verg',
    'interprataties:formele_stratigrafie',
    'interpretaties:gecodeerde_lithologie',
    'interpretaties:geotechnische_coderingen',
    'interpretaties:hydrogeologische_stratigrafie',
    'interpretaties:informele_hydrogeologische_stratigrafie',
    'interpretaties:informele_stratigrafie',
    'interpretaties:lithologische_beschrijvingen',
    'interpretaties:quartaire_stratigrafie',
]

for env in environments:
    # session = SessionFactory.get_session()
    session = requests.Session()

    # wfs = WebFeatureService(
    #     f'http://dov-geoserver-publiek-{env}-1.vm.cumuli.be:8080/geoserver/wfs',
    #     version='2.0.0')

    # for layer in wfs.contents:
    # while True:
    for layer in layers:
        workspace, layername = layer.split(':')

        timestamp = time.strftime('%H:%M:%S')
        sys.stdout.write(
            f'{timestamp} - Testing environment {env} with layer {layer} ... ')
        sys.stdout.flush()

        layer_failed = False
        failed_urls = []
        failed_nodes = []

        for node in range(1, 5):
            # wfs = WebFeatureService(
            #     f'http://dov-geoserver-publiek-{env}-{node}.vm.cumuli.be:8080/geoserver/wfs',
            #     version='2.0.0')

            url = (
                f'http://dov-geoserver-publiek-{env}-{node}.vm.cumuli.be:8080/'
                f'geoserver/{workspace}/wfs?version=2.0.0&request=GetFeature&'
                f'typeName={layername}&count=1&startIndex=10')

            r = session.get(url)

            success = 'Exception' not in r.text

            if not success:
                layer_failed = True
                failed_nodes.append(str(node))
                failed_urls.append('   ' + url)
                # print('      ' + r.text)

        if layer_failed:
            sys.stdout.write(
                f'FAILED on node(s) {", ".join(failed_nodes)}.\n')
            sys.stdout.write("\n".join(failed_urls) + '\n')
        else:
            sys.stdout.write('OK.\n')
