Classes and methods for boringen and interpetations
===================================================

Possible schema:

.. code-block:: python

   import pandas

   class DovSearch(object)
       def __init__(self, ):
           """instantiate class for certain location
           """
           pass

       def get_metadata(self, ):
           """get metadata from wfs
           """
           pass

       def get_data(self, location=None, query=None, columns=None):
           """get data from wfs and/or xml
           """
           self.location = location # add method to derive location from input
           self.query = query
           self.columns = columns # the attributes that one wants to retreive
                                  # this way a download of the XML is prevented
                                  # if not required
           # different steps to come to dataframe
           return dataframe_with_columns_of_interest

   class DovGrondwaterFilter(DovSearch):
       def __init__(self, ):
           """instantiate class for certain location

           """

           pass

       def get_data(location=None, query=None, columns=None, extra_argument=None):
           """for the filters one can add an additional argument to get 'observaties' or
           'kwaliteitsdata', joined with the location which is returned by default
           """
           pass

   class DovBoringen(DovSearch):
       def __init__(self, ):
           """instantiate class
           """

           pass

       def list_interpretations(self, ):
           """check which intepretations are available
           """
           return Interpretatie().defined_interpretations

       def get_interpretation(self, interpretation):
           """get data from wfs and/or xml for a certain interpretation

           Parameters
           ----------
           interpretation: string
                the selected intepretation

           """
           self.ip = globals()[interpretation]()
           df_boring .... get data from....
           data_ip ... get data from....
           df_ip = self.ip.get_interpretation(data_ip)
           # add method to join with where clause
           return df


   class Interpretatie(DovSearch):
       """class for interpretation related stuff
       """
       def __init__(self,):
           """instantiate class
           """
           self.defined_interpretations = ['InformeleStratigrafie',
                                           'FormeleStratigrafie',
                                           'Lithologische beschrijvingen',
                                           'GecodeerdeLithologie',
                                           'HydrogeologischeInterpretatie',
                                           'InformeleHydrogeologischeStratigrafie',
                                           'QuartaireStratigrafie',
                                           'GeotechnischeCoderingen',]


   class HydrogeologischeInterpretatie(Interpretatie):
       """class for interpretation of Hydrogeological Stratification
       """
       def __init__(self, location=None):
           """instantiate class for certain location

           location can be anything from coordinates (with buffer), bbox
           or polygon, default None
           """
           if location:
               self.location = location # add method to derive location from input
           self.headers = ['pkey_interpretatie',
                           'pkey_boring',
                           'pkey_sondering',
                           'diepte_laag_van',
                           'diepte_laag_tot',
                           'aquifer']

       def get_dataframe(self, input):
           """create dataframe from input

           """
           self.df = pd.DataFrame(input, columns=self.headers)

   """
   Examples
    --------
   >>> boring = DovBoringen()
   >>> boring_metadata = boring.get_metadata()
   >>> df_boring = boring.get_data(location, query, columns=[columns of interest])
   >>> print Interpretatie().defined_interpretations
   >>> interpretatie = HydrogeologischeInterpretatie()
   >>> df_interpretatie = interpretatie.get_data_from_boring(df_boring)
   >>> # alternatively
   >>> print Interpretatie().defined_interpretations
   >>> intepretatie = HydrogeologischeInterpretatie()
   >>> interpretatie_metadata = interpretatie.get_metadata()
   >>> df_interpetatie = intepretatie.get_data_interpretatie(location, query, columns=[columns of interest])
   """
