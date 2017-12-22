# -*- coding: utf-8 -*-
"""Module containing the basic DOV data types."""
import datetime
import types
from collections import OrderedDict

from owslib.etree import etree


class AbstractDovType(object):
    _fields = []

    def __init__(self, typename, pkey):
        self.typename = typename
        self.pkey = pkey
        self.data = dict(zip(self.get_columns(),
                             [None] * len(self.get_columns())))
        self.data['pkey_%s' % self.typename] = self.pkey

    @classmethod
    def from_wfs_element(cls, feature, ns):
        raise NotImplementedError('This should be implemented in a subclass.')

    @classmethod
    def from_wfs(cls, elements, ns):
        if type(elements) is str:
            elements = elements.encode('utf8')

        if type(elements) is bytes:
            tree = etree.fromstring(elements)

            for ft in tree.find('.//{http://www.opengis.net/gml}'
                                'featureMembers'):
                yield (cls.from_wfs_element(ft, ns))

        if type(elements) is list \
            or type(elements) is tuple \
            or isinstance(elements, types.GeneratorType):
            for el in elements:
                yield (cls.from_wfs_element(el, ns))

    @classmethod
    def get_columns(cls):
        return [f['name'] for f in cls._fields]

    @classmethod
    def get_fields(cls, source=('wfs', 'xml')):
        return OrderedDict(
            zip([f['name'] for f in cls._fields if f['source'] in source],
                [f for f in cls._fields if f['source'] in source]))

    @classmethod
    def to_df_array(cls, iterable):
        for item in iterable:
            yield (item.get_df_array())

    @classmethod
    def _parse(cls, fn, namespace, path, returntype):
        def typeconvert(x): return x

        if returntype == 'string':
            def typeconvert(x): return str(x).strip()
        elif returntype == 'float':
            def typeconvert(x): return float(x)
        elif returntype == 'date':
            def typeconvert(x): return datetime.datetime.strptime(
                x, '%Y-%m-%dZ').date()

        ns = '{%s}' % namespace
        text = fn('./' + ns + ('/' + ns).join(path.split('/')))
        if text is None:
            return None
        return typeconvert(text)

    def get_df_array(self):
        return [self.data[c] for c in self.get_columns()]


class Boring(AbstractDovType):
    _fields = [{
        'name': 'pkey_boring',
        'source': 'wfs',
        'sourcefield': 'fiche',
        'type': 'string'
    }, {
        'name': 'boornummer',
        'source': 'wfs',
        'sourcefield': 'boornummer',
        'type': 'string'
    }, {
        'name': 'x',
        'source': 'wfs',
        'sourcefield': 'X_mL72',
        'type': 'float'
    }, {
        'name': 'y',
        'source': 'wfs',
        'sourcefield': 'Y_mL72',
        'type': 'float'
    }, {
        'name': 'mv_mtaw',
        'source': 'xml',
        'sourcefield': '/boring/oorspronkelijk_maaiveld/waarde',
        'definition': 'Maaiveldhoogte in mTAW op dag dat de boring '
                      'uitgevoerd werd.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'start_boring_mtaw',
        'source': 'wfs',
        'sourcefield': 'Z_mTAW',
        'type': 'float'
    }, {
        'name': 'diepte_boring_van',
        'source': 'xml',
        'sourcefield': '/boring/diepte_van',
        'definition': 'Startdiepte van de boring (in meter).',
        'type': 'float',
        'notnull': True
    }, {
        'name': 'diepte_boring_tot',
        'source': 'wfs',
        'sourcefield': 'diepte_tot_m',
        'type': 'float'
    }, {
        'name': 'datum_aanvang',
        'source': 'wfs',
        'sourcefield': 'datum_aanvang',
        'type': 'date'
    }, {
        'name': 'uitvoerder',
        'source': 'wfs',
        'sourcefield': 'uitvoerder',
        'type': 'string'
    }, {
        'name': 'boorgatmeting',
        'source': 'xml',
        'sourcefield': '/boring/boorgatmeting/uitgevoerd',
        'definition': 'Is er een boorgatmeting uitgevoerd (ja/nee).',
        'type': 'boolean',
        'notnull': False
    }, {
        'name': 'diepte_methode_van',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/van',
        'definition': 'Bovenkant van de laag die met een bepaalde '
                      'methode aangeboord werd, in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'diepte_methode_tot',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/tot',
        'definition': 'Onderkant van de laag die met een bepaalde '
                      'methode aangeboord werd, in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'boormethode',
        'source': 'xml',
        'sourcefield': '/boring/details/boormethode/methode',
        'definition': 'Boormethode voor het diepte-interval.',
        'type': 'string',
        'notnull': False
    }]

    def __init__(self, pkey):
        super(Boring, self).__init__('boring', pkey)

    @classmethod
    def from_wfs_element(cls, el, ns):
        b = Boring(el.findtext('./{%s}fiche' % ns))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(el.findtext, ns,
                                               field['sourcefield'],
                                               field.get('type', None))

        return b
