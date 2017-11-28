Classes and methods for boringen and interpetations
===================================================

Possible schema:

.. code-block:: python

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


   class IpHydroStrat(DovSearch):
       """class for interpretation of Hydrogeological Stratification
       """
       def __init__(self, ):
           """instantiate 
           
           """
           pass
 
 