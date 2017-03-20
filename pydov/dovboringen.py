"""
This module handles the selection of borehole data from the DOV webservice.

It's development was made possible by the financing of Vlaio (Flanders, Belgium) and AGT n.v (www.agt.be).
"""
__author__ = ['Pieter Jan Haest', "Johan Van De Wauw"]
__copyright__ = 'Copyright 2017, DOV-Vlaanderen'
__credits__ = ["Stijn Van Hoey"]
__license__ = "MIT"
__version__ = '0.1'
__maintainer__ = "Pieter Jan Haest"
__email__ = "geo.haest@gmail.com"
__status__ = "Development"

from owslib.wfs import WebFeatureService
from owslib import fes
import xmltodict
import urllib2
import requests
import pandas as pd


class DOVVariableError(Exception):
    pass


class DovBoringen(object):

    def __init__(self, url='https://www.dov.vlaanderen.be/geoserver/wfs', version='2.0.0', layer='dov-pub:Boringen',
                 maxfeatures=10000, timeout=30, outputformat='xml', epsg='31370'):
        """ Initialize DovBoringen instance to read borehole data for selected locations in xml

        Parameters
        ----------
        url: str
            url string
        version: str
            the version on the wfs_boring
        layer: str
            the layer with the general borehole data
        maxfeatures: int
            the maximum number of features that will be obtained from the wfs_boring
        timeout: int
            time in seconds after which requests should time-out
        outputformat: str
            the format that is returned from the wfs_boring
        epsg: int
            the epsg code in which data should be retrieved. Default value for Lamber72: 31370
        """
        # define general wfs_boring info
        self.layer = layer
        self.outputformat = 'application/'+outputformat
        self.timeout = timeout
        self.wfs_boring = WebFeatureService(url=url, version=version)
        # check version
        self.version = self.wfs_boring.identification.version
        # check contents through: self.wfs_boring.contents['dov-pub:Boringen']
        self.maxfeatbool = False    # a boolean indicating that a limit exists on the queryable features
        self.srsname = 'urn:x-ogc:def:crs:EPSG:'+epsg

        try:
            server_maxfeatures = int(self.wfs_boring.constraints['DefaultMaxFeatures'].values[0])
            if server_maxfeatures < maxfeatures:
                self.maxfeatures = server_maxfeatures
                self.maxfeatbool = True
            else:
                self.maxfeatures = maxfeatures
        except:
            self.maxfeatures = maxfeatures



if __name__ == '__main__':
    dov = DovBoringen(maxfeatures=10)
    query_str = 'diepte_tot_m > 20'
    extracted_locations = dov.get_boringen(query_string=query_str, bbox=(160000, 200000, 178100, 215100))
    a = 1
    df_boringen = dov.get_boringen_data(extracted_locations)

