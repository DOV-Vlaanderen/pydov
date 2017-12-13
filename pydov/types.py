# -*- coding: utf-8 -*-
"""Module containing the basic DOV data types."""
import types

from owslib.etree import etree

from pydov.util.owsutil import parse


class AbstractDovType(object):
    def __init__(self, typename, pkey):
        self.typename = typename
        self.pkey = pkey
        self.data = dict(zip(self.get_columns(),
                             [None]*len(self.get_columns())))
        self.data['pkey_%s' % self.typename] = self.pkey

    @classmethod
    def from_wfs(cls, elements, ns):
        if type(elements) is str:
            elements = elements.encode('utf8')

        if type(elements) is bytes:
            tree = etree.fromstring(elements)

            for ft in tree.find('.//{http://www.opengis.net/gml}'
                                'featureMembers'):
                yield(cls.from_wfs_element(ft, ns))

        if type(elements) is list \
                or type(elements) is tuple \
                or isinstance(elements, types.GeneratorType):
            for el in elements:
                yield(cls.from_wfs_element(el, ns))

    def get_columns(self):
        return ['pkey_%s' % self.typename]

    @staticmethod
    def to_df_array(iterable):
        for item in iterable:
            yield(item.get_df_array())

    def get_df_array(self):
        return [self.data[c] for c in self.get_columns()]


class Boring(AbstractDovType):
    _fields = [{
            'name': 'pkey_boring',
            'source': 'wfs',
            'sourcefield': 'fiche'
        }, {
            'name': 'boornummer',
            'source': 'wfs',
            'sourcefield': 'boornummer'
        }, {
            'name': 'x',
            'source': 'wfs',
            'sourcefield': 'X_mL72'
        }, {
            'name': 'y',
            'source': 'wfs',
            'sourcefield': 'Y_mL72'
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
            'sourcefield': 'Z_mTAW'
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
            'sourcefield': 'diepte_tot_m'
        }, {
            'name': 'datum_aanvang',
            'source': 'wfs',
            'sourcefield': 'datum_aanvang'
        }, {
            'name': 'uitvoerder',
            'source': 'wfs',
            'sourcefield': 'uitvoerder'
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

    @staticmethod
    def get_fields(source=('wfs', 'xml')):
        return dict(
            zip([f['name'] for f in Boring._fields if f['source'] in source],
                [f for f in Boring._fields if f['source'] in source]))

    @staticmethod
    def from_wfs_element(el, ns):
        b = Boring(el.findtext('./{%s}fiche' % ns))
        b.data['boornummer'] = parse(el.findtext, ns, 'boornummer')
        b.data['x'] = parse(el.findtext, ns, 'X_mL72')
        b.data['y'] = parse(el.findtext, ns, 'Y_mL72')
        b.data['start_boring_mtaw'] = parse(el.findtext, ns, 'Z_mTAW')
        b.data['diepte_boring_tot'] = parse(el.findtext, ns, 'diepte_tot_m')
        b.data['datum_aanvang'] = parse(el.findtext, ns, 'datum_aanvang')
        b.data['uitvoerder'] = parse(el.findtext, ns, 'uitvoerder')
        return b

    @staticmethod
    def get_columns():
        return [f['name'] for f in Boring._fields]

