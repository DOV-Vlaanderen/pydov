"""Module giving some examples how to use PyDOV to query boreholes."""


def get_description():
    """The description gives information about the Boring type."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch

    gwfilter = GrondwaterFilterSearch()
    print(gwfilter.get_description())


def get_fields():
    """The fields give details about what information is available for a
    Boring object."""
    from pydov.search.boring import BoringSearch

    b = BoringSearch()
    fields = b.get_fields()
    for f in fields.values():
        print(f['name'])
        print(' ', f['definition'])
        print('   datatype:', f['type'])
        print('   mandatory:', f['notnull'])
        if 'values' in f:
            print('   possible values:', '; '.join(
                ["'%s'" % i for i in f['values']]))
        print('   cost: ', f['cost'])
        print('')


def get_groundwaterfilters_in_hamme():
    """Get all details of the boreholes where 'gemeente' is 'Hamme'."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsEqualTo

    gwfilter = GrondwaterFilterSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Hamme')
    df = gwfilter.search(query=query)
    print(df)

def get_filter_coordinates_in_gent():
    """Get the filter coordinates of all boreholes in Ghent."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsEqualTo

    gwfilter = GrondwaterFilterSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Gent')
    df = gwfilter.search(query=query,
                  return_fields=(['pkey_filter', 'x', 'y', 'meetnet']))
    print(df)


def get_filter_meetnet_in_boortmeerbeek():
    """Get the filter meetnet description (wfs) and meetnet_codes (xml)"""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsEqualTo

    gwfilter = GrondwaterFilterSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Boortmeerbeek')
    df = gwfilter.search(query=query,
                  return_fields=(['pkey_filter',
                                  'meetnet',
                                  'meetnet_code']))
    print(df)

def get_filters_in_bounding_box():
    """Get all the filters within the given bounding box."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch

    gwfilter = GrondwaterFilterSearch()
    df = gwfilter.search(
        location=(93378, 168009, 94246, 169873)
    )
    print(df)

def get_INBO_filters_in_bounding_box():
    """Get all details of the filters of meetnet 9 INBO,
    within the given bounding box."""
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsLike

    gwfilter = GrondwaterFilterSearch()
    query = PropertyIsLike(
        propertyname='meetnet', literal='meetnet 9%')
    df = gwfilter.search(
        location=(87676, 163442, 91194, 168043),
        query=query
    )
    print(df)

def get_filters_depth_or_primary():
    """Get all groundwater screesn in Hamme that have a value for length_filter
    and either belong to the primary meetnet of VMM or that have a depth
    bottom screen less than 3 meter.
    """
    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from owslib.fes import PropertyIsLessThanOrEqualTo
    from owslib.fes import PropertyIsLike
    from owslib.fes import PropertyIsEqualTo
    from owslib.fes import PropertyIsNull
    from owslib.fes import And
    from owslib.fes import Or
    from owslib.fes import Not

    gwfilter = GrondwaterFilterSearch()
    query = And([PropertyIsEqualTo(propertyname='gemeente',
                                   literal='Hamme'),
                 Not([PropertyIsNull(propertyname='lengte_filter')]),
                 Or([PropertyIsLike(propertyname='meetnet',
                                    literal='meetnet 1%'),
                     PropertyIsLessThanOrEqualTo(
                         propertyname='diepte_onderkant_filter',
                         literal='3')])])
    df = gwfilter.search(query=query)
    print(df)

if __name__ == '__main__':
    # Comment out to skip these examples:
    get_description()
    # get_fields()

    # Uncomment one of these to see the output:
    #
    #get_groundwaterfilters_in_hamme()
    #get_filter_coordinates_in_gent()
    #get_filter_meetnet_in_boortmeerbeek()
    #get_filters_in_bounding_box()
    #get_INBO_filters_in_bounding_box()
    get_filters_depth_or_primary()
