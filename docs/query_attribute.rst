.. _query_attribute:

=============================
Query on attribute properties
=============================

To find data based on one or more of its attribute values, we can use the ``query`` parameter of the search objects. This parameter takes a filter expression as its argument, based on the OGC filter expressions from the OWSLib library.

.. _available_attribute_fields:

Available attribute fields
**************************
The list of available attributes (or: fields) depends on the dataset you want to query and can be retrieved with the ``get_fields`` method. This results in a dictionary with for each of the fields a new dictionary with more information about the field.

For each field, the following information is available:

name
    The name of the field.

    Example: ``'methode'``

definition
    The definition of the field.

    Example: ``'De methode waarmee de boring uitgevoerd werd. Heeft als waarde 'onbekend' indien de methode niet gekend is.'``

cost
    The resource cost (in time) to request this field as part of the return fields. Is either '1' (no additional cost) or '10' (cost of an implicit XML download per result feature).

    Example: ``1``

notnull
    Whether the field is mandatory (True) or optional (False).

    Example: ``True``

query
    Whether the field can be used in an attribute query.

    Example: ``True``

type
    The datatype of the values of this field.

    Example: ``'string'``

values
    (Optional) In case the field has a list of possible values, they are listed here as a dictionary mapping the values to a definition (if available).

    Example: ``{'Aa': 'Formatie van Aalter', 'AaBe': 'Lid van Beernem (Formatie van Aalter)', 'AaOe': 'Lid van Oedelem (Formatie van Aalter)'}``

Example
-------
To get the name and definition of all attributes that are available for use in a search query for boreholes (`query` is True), you'd use:

::

    from pydov.search.boring import BoringSearch
    boringsearch = BoringSearch()

    fields = boringsearch.get_fields()
    for f in fields:
        if fields[f]['query']:
            print(fields[f]['name'], '-', fields[f]['definition'])

Which would result in:

::

    generated_id - Oplopend uniek volgnummer ter identificatie (intern en niet-stabiel).
    id - Volgnummer ter identificatie (intern en niet-stabiel).
    boornummer - Het boornummer (ook gekend als proefnummer) van de boring.
    pkey_boring - Permanente URL die verwijst naar de gegevens van de boring op de website. Voeg '.xml' toe om een XML voorstelling van deze gegevens te verkrijgen.
    rapport - URL die verwijst naar het rapport van de boring in PDF formaat.
    diepte_boring_tot - Maximumdiepte van de boring ten opzichte van het aanvangspeil, in meter.
    datum_aanvang - Datum waarop men de boring gestart is.
    namen - Alternatieve benamingen voor de boring.
    putnummer - Het GW_ID (ook gekend als putnummer) van de put waaraan de boring gekoppeld is. Wanneer dit veld leeg is is de boring niet gekoppeld aan een put.
    x - De x-coördinaat van de boring in het Lambert72 coördinaatsysteem (in meter, EPSG:31370).
    y - De y-coördinaat van de boring in het Lambert72 coördinaatsysteem (in meter, EPSG:31370).
    start_boring_mtaw - De hoogte van het aanvangspeil van de boring in het TAW stelsel (in meter).
    gemeente - De gemeente waarin de boring gelegen is.
    uitvoerder - De organisatie die de boring uitvoerde. Heeft als waarde 'onbekend' indien de uitvoerder niet gekend is.
    doel - Het doel van de boring.
    methode - De methode waarmee de boring uitgevoerd werd. Heeft als waarde 'onbekend' indien de methode niet gekend is.
    erkenning - In het kader van welke discipline de boring werd uitgevoerd. Deze codelijst bevat de verschillende disciplines van erkende boorbedrijven uit artikel 6, 7°, a) van VLAREL.
    opdrachtgever - De organisatie die de opdracht gaf om de boring uit te voeren.  Heeft als waarde 'onbekend' indien de opdrachtgever niet gekend is.
    informele_stratigrafie - Geeft aan of er aan de boring minstens één interpretatie van het type 'informele stratigrafie' gekoppeld is.
    formele_stratigrafie - Geeft aan of er aan de boring minstens één interpretatie van het type 'formele stratigrafie' gekoppeld is.
    lithologische_beschrijving - Geeft aan of er aan de boring minstens één interpretatie van het type 'lithologische beschrijving' gekoppeld is.
    gecodeerde_lithologie - Geeft aan of er aan de boring minstens één interpretatie van het type 'gecodeerde lithologie' gekoppeld is.
    hydrogeologische_stratigrafie - Geeft aan of er aan de boring minstens één interpretatie van het type 'hydrogeologische stratigrafie' gekoppeld is.
    quartaire_stratigrafie - Geeft aan of er aan de boring minstens één interpretatie van het type 'quartaire stratigrafie' gekoppeld is.
    geotechnische_codering - Geeft aan of er aan de boring minstens één interpretatie van het type 'geotechnische codering' gekoppeld is.
    informele_hydrostratigrafie - Geeft aan of er aan de boring minstens één interpretatie van het type 'informele hydrostratigrafie' gekoppeld is.
    doorheen_quartair - Geeft aan of de boring dieper ging dan de grens van het Quartair en het Neogeen/Paleogeen (Tertiair). Dit veld is enkel ingevuld indien er minstens één interpretatie van het type 'formele stratigrafie' gekoppeld is aan de boring én het Quartair geïnterpreteerd werd.
    dikte_quartair - Dit veld geeft de dikte weer van het Quartair (in meter). Dit is een getal met twee decimalen, soms voorafgegaan door < of >= (bv. >= 10.00).
    tertiair_onder_quartair - Indien 'doorheen_quartair' true is bevat dit veld de afkorting van de eerste lithostratigrafische eenheid van het Neogeen/Paleogeen (Tertiair) die voorkomt onder het Quartair.
    opdrachten - De DOV-opdracht(en) waaraan de boring gekoppeld is.

Other information about each field includes its datatype (`type`), cost to use it as return field (`cost`) or whether it is mandatory (`notnull`):

::

    fields['diepte_boring_tot']

::

    {'cost': 1,
     'definition': 'Maximumdiepte van de boring ten opzichte van het aanvangspeil, in meter.',
     'name': 'diepte_boring_tot',
     'notnull': False,
     'type': 'float'}

Some fields additionally have a list of possible values (`values`):

::

    fields['methode']['values'].keys()

::

    ['avegaarboring',
     'droge boring',
     'edelmanboring',
     'geen boring',
     'gestoken boring',
     'graafmachine',
     'handboring',
     'kernboring',
     'lansen',
     'lepelboring',
     'luchthamer',
     'luchthevelboren of air-lift boren',
     'meerdere technieken',
     'omgek. spoelboring',
     'onbekend',
     'pulsboring',
     'ramguts',
     'ramkernboring',
     'rollerbit',
     'slagboring',
     'spade',
     'spiraalboring',
     'spoelboring',
     'steenboring',
     'trilboring',
     'voorput',
     'zuigboring']

Sometimes the definition can be used as a (human readable) label for the (machine readable) code in the dataframe. This allows creating an extra column with the mapped labels:

::

    from pydov.search.interpretaties import FormeleStratigrafieSearch
    itp = FormeleStratigrafieSearch()

    fields['lid1']
    # {'cost': 10,
    #  'definition': 'eerste eenheid van de laag formele stratigrafie',
    #  'name': 'lid1',
    #  'notnull': False,
    #  'query': False,
    #  'type': 'string',
    #  'values': {'Aa': 'Formatie van Aalter',
    #   'AaBe': 'Lid van Beernem (Formatie van Aalter)',
    #   'AaOe': 'Lid van Oedelem (Formatie van Aalter)',
    #   'Bb': 'Formatie van Bolderberg',
    #   'BbGe': 'Lid van Genk (Formatie van Bolderberg)',
    #   'BbHo': 'Lid van Houthalen (Formatie van Bolderberg)',
    #   'BbOp': 'Lid van Opitter (Formatie van Bolderberg)',
    #   'Bc': 'Formatie van Berchem',
    #   ..}
    # }

    df['lid1_label'] = df['lid1'].map(fields['lid1']['values'])
    df['lid2_label'] = df['lid2'].map(fields['lid2']['values'])

    print(df[['diepte_laag_van', 'diepte_laag_tot', 'lid1',
         'lid1_label', 'relatie_lid1_lid2', 'lid2', 'lid2_label']].to_string())
    #    diepte_laag_van  diepte_laag_tot lid1           lid1_label relatie_lid1_lid2 lid2            lid2_label
    # 0              0.0             3.00    Q  Quartaire afzetting                 T    Q   Quartaire afzetting
    # 1              3.0            14.05    U             Onbekend                 T   Bc  Formatie van Berchem


Using OGC filter expressions
****************************
An attribute query consists of an OGC filter predicate, a query field (`propertyname`) and a literal value (`literal`). pydov uses the OGC filter predicates from the OWSLib library, defined in the owslib.fes package.

Note that the literal value is always expressed as a string, even if the field that is being searched is of a numeric, date or boolean type (dates should be expressed in the 'YYYY-mm-dd' format).


The following OGC filters are relevant for string, numeric, date or boolean attributes:

PropertyIsEqualTo
    Search for exact matches.

    Example: ``PropertyIsEqualTo(propertyname='methode', literal='ramkernboring')``

    Example: ``PropertyIsEqualTo(propertyname='diepte_boring_tot', literal='10')``

    Example: ``PropertyIsEqualTo(propertyname='datum_aanvang', literal='2014-01-01')``

    Example: ``PropertyIsEqualTo(propertyname='quartaire_stratigrafie', literal='True')``

PropertyIsNotEqualTo
    Search for values different from a given literal. Does not include empty values.

    Example: ``PropertyIsNotEqualTo(propertyname='methode', literal='onbekend')``

PropertyIsNull
    Search for empty values. This filter only requires a propertyname.

    Example: ``PropertyIsNull(propertyname='gemeente')``


The following OGC filters are relevant for string attributes:

PropertyIsLike
    Search for fuzzy matches. You can use the '_' wildcard to represent a single character and the '%' wildcard to represent multiple characters.

    Example: ``PropertyIsLike(propertyname='methode', literal='lucht%')``


The following OGC filters are relevant for numeric or date attributes:

PropertyIsLessThan
    Search for values strictly less than (or: before) the given literal.

    Example: ``PropertyIsLessThan(propertyname='diepte_boring_tot', literal='10')``

PropertyIsLessThanOrEqualTo
    Search for values less than (or: before) or equal to the given literal.

    Example: ``PropertyIsLessThanOrEqualTo(propertyname='datum_aanvang', literal='2014-12-31')``

PropertyIsGreaterThan
    Search for values strictly greater than (or: after) the given literal.

    Example: ``PropertyIsGreaterThan(propertyname='diepte_boring_tot', literal='10')``

PropertyIsGreaterThanOrEqualTo
    Search for values greater than (or: after) or equal to the given literal.

    Example: ``PropertyIsGreaterThanOrEqualTo(propertyname='datum_aanvang', literal='2015-01-01')``

PropertyIsBetween
    Search for values greater than (or: after) or equal to the lower boundary and less than (or: before) or equal to the upper boundary. This filter requires two literal values as the lower and upper boundaries. Boundaries are inclusive.

    Example: ``PropertyIsBetween(propertyname='diepte_boring_tot', lower='20', upper='50')``

    Example: ``PropertyIsBetween(propertyname='datum_aanvang', lower='2014-01-01', upper='2014-12-31')``


Logically combining filter expressions
**************************************
You can combine different OGC filter expressions in one query by using the `And`, `Or` and `Not` predicates from the owslib.fes package.

Each of `And`, `Or` and `Not` take a list as argument, in the case of `And` and `Or` the list should consist of at least two items. Each item can be a simple OGC filter expression or another `And`, `Or` or `Not` expression, so you can nest different levels of filter expressions.

And
    Return results that match all listed filters.

    Example: ``And([PropertyIsLessThan(propertyname='diepte_boring_tot', literal='10'), PropertyIsGreaterThan(propertyname='datum_aanvang', literal='2014-12-31')])``

Or
    Return results that match one or more listed filters.

    Example: ``Or([PropertyIsLessThan(propertyname='diepte_boring_tot', literal='10'), PropertyIsGreaterThan(propertyname='datum_aanvang', literal='2014-12-31')])``

Not
    Return results that do not match any of the listed filters.

    Example: ``Not([PropertyIsLike(propertyname='methode', literal='lucht%')])``

Example
-------
An example of an advanced query using a nested combination of logical filter expressions:

::

    from owslib.fes import And, Or, Not
    from owslib.fes import PropertyIsEqualTo, PropertyIsLike, PropertyIsNull

    from pydov.search.boring import BoringSearch
    boringsearch = BoringSearch()

    query = And([PropertyIsEqualTo(propertyname='gemeente',
                                   literal='Antwerpen'),
                 Or([Not([PropertyIsNull(propertyname='putnummer')]),
                    PropertyIsLike(propertyname='doel',
                                   literal='Grondwater%'),
                    PropertyIsEqualTo(propertyname='erkenning',
                                      literal='2. Andere grondwaterwinningen')]
                   )]
               )
    df = boring.search(query=query)


Using custom filter expressions
*******************************

pydov adds two custom filter expressions to the available set from OGC described above. They can be imported from the pydov.util.query module.


Query using lists
-----------------

pydov extends the default OGC filter expressions described above with a new expression `PropertyInList` that allows you to use lists (of strings) in search queries.

The `PropertyInList` internally translates to a `PropertyIsEqualTo` and is relevant for string, numeric, date or boolean attributes:

PropertyInList
    Search for one of a list of exact matches.

    Internally this is translated to ``Or([PropertyIsEqualTo(), PropertyIsEqualTo(), ...])``.

    Example: ``PropertyInList(propertyname='methode', list=['ramkernboring', 'spoelboring', 'spade'])``


Join different searches
-----------------------

The `Join` expression allows you to join multiple searches together. This allows combining results from different datasets to get the results you're looking for.

Join
    Join searches together using a common attribute. Instead of a propertyname and a literal (or a list of literals), this expression takes a Pandas dataframe and a join column. The join column should be a column that exists in the dataframe and is one of the attributes of the type that is being searched.

    Example: ``Join(dataframe=df_boringen, join_column='pkey_boring')``

The following example returns all the lithological descriptions of boreholes that are at least 20 meters deep (note that this is different from 'lithological descriptions with a depth of at least 20m'):

::

    from pydov.util.query import Join

    from pydov.search.boring import BoringSearch
    from pydov.search.interpretaties import LithologischeBeschrijvingenSearch

    bs = BoringSearch()
    ls = LithologischeBeschrijvingenSearch()

    boringen = bs.search(query=PropertyIsGreaterThan('diepte_tot_m', '20'),
                         return_fields=('pkey_boring',))

    lithologische_beschrijvingen = ls.search(query=Join(boringen, 'pkey_boring'))

`Join` expressions can be logically combined with other filter expressions, for example to further restrict the resultset:

::

    from owslib.fes import And
    from owslib.fes import PropertyIsEqualTo

    from pydov.util.query import Join

    from pydov.search.boring import BoringSearch
    from pydov.search.interpretaties import LithologischeBeschrijvingenSearch

    bs = BoringSearch()
    ls = LithologischeBeschrijvingenSearch()

    boringen = bs.search(query=PropertyIsGreaterThan('diepte_tot_m', '20'),
                         return_fields=('pkey_boring',))

    lithologische_beschrijvingen = ls.search(query=And([Join(boringen, 'pkey_boring'),
                                                        PropertyIsEqualTo('betrouwbaarheid_interpretatie', 'goed')]))
