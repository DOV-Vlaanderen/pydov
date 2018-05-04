"""Module giving some examples how to use PyDOV to query interpretations."""


def informele_stratigrafie_get_description():
    """The description gives information about the Informele Stratigrafie
    type."""
    from pydov.search.interpretaties import InformeleStratigrafieSearch

    ifs = InformeleStratigrafieSearch()
    print(ifs.get_description())


def informele_stratigrafie_get_fields():
    """The fields give details about what information is available for a
    Informele Stratigrafie object."""
    from pydov.search.interpretaties import InformeleStratigrafieSearch

    ifs = InformeleStratigrafieSearch()
    fields = ifs.get_fields()
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


def get_informele_stratigrafie_in_bounding_box():
    """Get all the boreholes within the given bounding box."""
    from pydov.search.interpretaties import InformeleStratigrafieSearch

    ifs = InformeleStratigrafieSearch()
    df = ifs.search(
        location=(151650, 214675, 151750, 214775)
        # return_fields=['pkey_interpretatie', 'pkey_boring', 'pkey_sondering',
        #                'Proeffiche', 'gemeente']
    )
    print(df)


if __name__ == '__main__':
    # Comment out to skip these examples:
    # informele_stratigrafie_get_description()
    informele_stratigrafie_get_fields()

    # Uncomment one of these to see the output:
    #
    get_informele_stratigrafie_in_bounding_box()
