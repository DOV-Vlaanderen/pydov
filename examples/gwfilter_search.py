"""Module giving some examples how to use PyDOV to query boreholes."""


def get_description():
    """The description gives information about the Boring type."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch

    gwfilter = GrondwaterFilterSearch()
    print(gwfilter.get_description())

def get_groundwaterfilters_in_hamme():
    """Get all details of the boreholes where 'gemeente' is 'Herstappe'."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsEqualTo

    gwfilter = GrondwaterFilterSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Hamme')
    df = gwfilter.search(query=query)
    print(df)

if __name__ == '__main__':
    # Comment out to skip these examples:
    get_description()
    # get_fields()

    # Uncomment one of these to see the output:
    #
    get_groundwaterfilters_in_hamme()
    # get_borehole_depth_in_gent()
    # get_deep_boreholes()
    # get_groundwater_related_boreholes_in_antwerp()
    # get_boreholes_in_bounding_box()
    # get_deep_boreholes_in_bounding_box()
    # get_borehole_purpose_in_blankenberge()
