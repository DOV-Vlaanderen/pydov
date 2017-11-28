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

       def get_data(self, ):
           """get data from wfs and/or xml
           """
           pass
   
   
   class DovBoringen(DovSearch):
       def __init__(self, location):
           """instantiate class for certain location
           
           location can be anything from coordinates (with buffer), bbox
           or polygon
           """
           self.location = location # add method to derive location from input
           pass

       def list_interpretations(self, ):
           """check which intepretations are available
           """

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
           df_ip = self.ip.get_interpretation(data)
           # add method to join with where clause
           return df


   class HydrogeologischeStratigrafie(DovSearch):
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
   >>> boring = DovBoringen(location)
   >>> boring_metadata = boring.get_metadata()
   >>> boring_data = boring.get_data()
   >>> df_iphydro = boring.get_interpretation('HydrogeologischeStratigrafie')
   >>> # alternatively
   >>> intepretatie = HydrogeologischeStratigrafie(location)
   >>> interpretatie_metadata = interpretatie.get_metadata()
   >>> interpretatie_data = intepretatie.get_data()
   >>> df_iphydro = interpretatie.get_interpretation(interpretatie_data)
   
   """ 
   
   