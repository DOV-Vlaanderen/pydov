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

    def __init__(self, ):
        """ Initialize DovBoringen instance to read borehole data for selected locations in xml
        """


if __name__ == '__main__':
    dov = DovBoringen(maxfeatures=10)
    query_str = 'diepte_tot_m > 20'
    extracted_locations = dov.get_boringen(query_string=query_str, bbox=(160000, 200000, 178100, 215100))
    a = 1
    df_boringen = dov.get_boringen_data(extracted_locations)

