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

        # define variables
        self.interpretations = ['gecodeerde_lithologie', 'geotechnische_codering', 'hydrogeologische_stratigrafie',
                                'informele_hydrostratigrafie', 'informele_stratigrafie', 'lithologische_beschrijving', ]
        self.property_names = ['diepte_tot_m', 'dikte_quartair', 'formele_stratigrafie', 'gecodeerde_lithologie',
                               'geotechnische_codering', 'hydrogeologische_stratigrafie', 'informele_hydrostratigrafie',
                               'informele_stratigrafie', 'lithologische_beschrijving', ]

    def get_boringen(self, query_string='', bbox=None, add_props=[]):
        """Query the wfs_boring for a all boreholes within a selected bounding box or given constraints.

        A dataframe containing the selected variables is returned. The following variables are always included:
        'boornummer', 'fiche', 'X_ml72', 'Y_ml72', 'Z_mTAW', 'methode', 'diepte_tot_m', 'dikte_quartair',
        'formele_stratigrafie', 'gecodeerde_lithologie', 'geotechnische_codering', 'hydrogeologische_stratigrafie',
        'informele_hydrostratigrafie', 'informele_stratigrafie', 'lithologische_beschrijving'
         Additional variables from the xml can be selected by providing the PropertyName in the list of add_props.
        The following variables are remapped to a more readable name in the resulting dataframe:
        {fiche: url_data, X_ml72: x, Y_ml72: y, Z_mTAW: z_mv}.

        Parameters:
        -----------
        query_string: str
            A string containing the query that will be used as constrained in the WFS call
        bbox: tuple of floats
            The X, Y coordinates of the bounding box as (xmin, ymin, xmax, ymax)
        add_props: list of strings
            A list with the PropertyNames of attributes in the queried layer that need to be selected in addition
            to the default ones

        Return:
        -------
        boringen_df: dataframe
            A dataframe with the selected attributes of the selected borehole locations

        """
        # extract data with user-defined column names
        user_defined = ['boornummer', 'url_data', 'x', 'y', 'z_mv', 'methode']
        dov_defined = ['boornummer', 'fiche', 'X_mL72', 'Y_mL72', 'Z_mTAW', 'methode']
        # get list with queried properties (different for version 1.1.0 and 2.0.0):
        variables1 = dov_defined + self.property_names + add_props
        variables2 = ['dov-pub:' + x for x in variables1]
        propertynames = variables1 if self.version == '1.1.0' else variables2
        # query the wfs layer for the given constraints in the bounding box
        filterxml = self.compose_query(query_string, bbox, self.wfs_filters)
        response = self.wfs_boring.getfeature(typename=self.layer,
                                              propertyname=propertynames,  # gives service exception for version 1.1.0
                                              maxfeatures=self.maxfeatures,
                                              # filter=filterxml,           # took ages to query, bbox is faster
                                              bbox=bbox,
                                              # outputFormat=self.outputformat,  # xml is only option and possible error
                                              # srsname=self.srsname  # does not work for version 2.0.0
                                              )
        if self.version == '1.1.0':
            boringen_df = pd.DataFrame(self.parse_wfs(response, self.layer, self.version),
                                       columns=variables1
                                       ).rename(columns=dict(zip(dov_defined, user_defined)))
        elif self.version == '2.0.0':
            boringen_df = pd.DataFrame(self.parse_wfs(response, self.layer, self.version),
                                       columns=variables2
                                       ).rename(columns=dict(zip(['dov-pub:'+x for x in dov_defined], user_defined)))
        return boringen_df


if __name__ == '__main__':
    dov = DovBoringen(maxfeatures=10)
    query_str = 'diepte_tot_m > 20'
    extracted_locations = dov.get_boringen(query_string=query_str, bbox=(160000, 200000, 178100, 215100))
    a = 1
    df_boringen = dov.get_boringen_data(extracted_locations)

