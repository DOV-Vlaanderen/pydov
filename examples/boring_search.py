"""Module giving some examples how to use PyDOV to query boreholes."""


def get_description():
    """The description gives information about the Boring type."""
    from pydov.search import BoringSearch

    b = BoringSearch()
    print(b.get_description())


def get_fields():
    """The fields give details about what information is available for a
    Boring object."""
    from pydov.search import BoringSearch

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


def get_boreholes_in_herstappe():
    """Get all details of the boreholes where 'gemeente' is 'Herstappe'."""
    from pydov.search import BoringSearch
    from owslib.fes import PropertyIsEqualTo

    b = BoringSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Herstappe')
    df = b.search(query=query)
    print(df)


def get_borehole_depth_in_gent():
    """Get the borehole depths of all boreholes in Ghent."""
    from pydov.search import BoringSearch
    from owslib.fes import PropertyIsEqualTo

    b = BoringSearch()
    query = PropertyIsEqualTo(propertyname='gemeente',
                              literal='Gent')
    df = b.search(query=query,
                  return_fields=('diepte_boring_tot',))
    print(df)


def get_deep_boreholes():
    """Get all details of the boreholes with a depth of at least 2000m."""
    from pydov.search import BoringSearch
    from owslib.fes import PropertyIsGreaterThanOrEqualTo

    b = BoringSearch()
    query = PropertyIsGreaterThanOrEqualTo(
        propertyname='diepte_boring_tot', literal='2000')
    df = b.search(query=query)
    print(df)


def get_groundwater_related_boreholes_in_antwerp():
    """Get all groundwater-related boreholes in Antwerp.

    These are the boreholes where 'gemeente' is 'Antwerp' and either
    'putnummer' is not empty or 'doel' starts with 'Grondwater' or
    'erkenning' equals '2. Andere grondwaterwinningen'.
    """
    from pydov.search import BoringSearch
    from owslib.fes import PropertyIsLike
    from owslib.fes import PropertyIsEqualTo
    from owslib.fes import PropertyIsNull
    from owslib.fes import And
    from owslib.fes import Or
    from owslib.fes import Not

    b = BoringSearch()
    query = And([PropertyIsEqualTo(propertyname='gemeente',
                                   literal='Antwerpen'),
                 Or([Not([PropertyIsNull(propertyname='putnummer')]),
                     PropertyIsLike(propertyname='doel',
                                    literal='Grondwater%'),
                     PropertyIsEqualTo(propertyname='erkenning',
                                       literal='2. Andere '
                                               'grondwaterwinningen')])])
    df = b.search(query=query)
    print(df)


def get_boreholes_in_bounding_box():
    """Get all the boreholes within the given bounding box."""
    from pydov.search import BoringSearch

    b = BoringSearch()
    df = b.search(
        location=(151650, 214675, 151750, 214775)
    )
    print(df)


if __name__ == '__main__':
    # Comment out to skip these examples:
    get_description()
    get_fields()

    # Uncomment one of these to see the output:
    #
    # get_boreholes_in_herstappe()
    # get_borehole_depth_in_gent()
    # get_deep_boreholes()
    # get_groundwater_related_boreholes_in_antwerp()
    # get_boreholes_in_bounding_box()
