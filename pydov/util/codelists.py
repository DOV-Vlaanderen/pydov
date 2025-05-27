import warnings
from pydov.search.abstract import AbstractCommon
from pydov.util.dovutil import (
    build_dov_sparql_request, get_remote_url, get_sparql_xml)
from pydov.util.errors import RemoteFetchError, XsdFetchWarning
from pydov.util.hooks import HookRunner

from owslib.etree import etree


class MemoryCache(object):
    cache = {}

    @staticmethod
    def get(key, fn, *args, **kwargs):
        if key not in MemoryCache.cache:
            MemoryCache.cache[key] = fn(*args, **kwargs)

        return MemoryCache.cache.get(key)


class CodeListItem(object):
    def __init__(self, code, label):
        self.code = code
        self.label = label


class AbstractCodeList(object):
    def __init__(self):
        self.items = []

    def get_values(self):
        if len(self.items) > 0:
            return dict((item.code, item.label) for item in self.items)


class AbstractResolvableCodeList(AbstractCommon, AbstractCodeList):
    def __init__(self, datatype):
        super().__init__()
        self.datatype = datatype

    def get_id(self):
        raise NotImplementedError

    def get_remote_codelist(self):
        raise NotImplementedError

    def resolve(self):
        raise NotImplementedError


class OsloCodeList(AbstractResolvableCodeList):
    def __init__(self, conceptscheme, datatype):
        super().__init__(datatype)
        self.conceptscheme = conceptscheme
        self._codelist = None

    def get_id(self):
        return f'{self.conceptscheme}.xml'

    def build_sparql_query(self):
        return """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX conceptscheme:
            <https://data.bodemenondergrond.vlaanderen.be/id/conceptscheme/>

            SELECT ?code ?label ?definition
            WHERE {{
            ?s skos:inScheme conceptscheme:{} .
            ?s skos:notation ?code .
            ?s skos:prefLabel ?label .
            ?s skos:note ?definition .
            }}
        """.format(self.conceptscheme)

    def get_remote_codelist(self):
        request = build_dov_sparql_request(self.build_sparql_query())

        response = HookRunner.execute_inject_meta_response(request.url)

        if response is None:
            try:
                response = MemoryCache.get(
                    self.get_id(), get_sparql_xml, request)
            except RemoteFetchError:
                warnings.warn(
                    "Failed to fetch remote sparql data, metadata will "
                    "be incomplete.", XsdFetchWarning)
                response = None

        HookRunner.execute_meta_received(request.url, response)

        return response

    def _get_rdf_codelist_items(self):
        if self._codelist is not None:
            tree = etree.fromstring(self._codelist)

            tree_solutions = tree.findall(
                './/{http://www.w3.org/2005/sparql-results#}solution'
            )

            for s in tree_solutions:
                code = s.find(
                    './/{http://www.w3.org/2005/sparql-results#}binding['
                    '{http://www.w3.org/2005/sparql-results#}variable="code"]'
                    '/{http://www.w3.org/2005/sparql-results#}value').text
                label = s.find(
                    './/{http://www.w3.org/2005/sparql-results#}binding['
                    '{http://www.w3.org/2005/sparql-results#}variable="label"]'
                    '/{http://www.w3.org/2005/sparql-results#}value').text
                yield CodeListItem(code, label)

    def resolve(self):
        self._codelist = self.get_remote_codelist()
        self.items = list(self._get_rdf_codelist_items())

    def get_values(self):
        self.resolve()
        return super().get_values()


class XsdType(AbstractResolvableCodeList):
    """Class for specifying an XSD type from an XSD schema. This will be
    resolved at runtime in a list of possible values and their definitions."""

    def __init__(self, xsd_schema, typename, datatype):
        """Initialise a XSD type reference.

        Parameters
        ----------
        xsd_schema : str
            URL of XSD schema record containing the specified typename.
        typename : str
            Name of the type.

        """
        super().__init__(datatype)

        self.source_url = xsd_schema
        self.typename = typename
        self._schema = None

    def get_id(self):
        return self.source_url.split('/')[-1]

    def get_remote_codelist(self):
        """Request the XSD schema from DOV webservices and return it.

        Parameters
        ----------
        url : str
            URL of the XSD schema to download.

        Returns
        -------
        xml : bytes
            The raw XML data of this XSD schema as bytes.

        """
        response = HookRunner.execute_inject_meta_response(self.source_url)

        if response is None:
            try:
                response = MemoryCache.get(
                    self.get_id(), get_remote_url, self.source_url)
            except RemoteFetchError:
                warnings.warn(
                    "Failed to fetch remote XSD schema, metadata will "
                    "be incomplete.", XsdFetchWarning)
                response = None

        HookRunner.execute_meta_received(self.source_url, response)

        return response

    def _get_xsd_enum_values(self):
        if self._schema is not None:
            tree = etree.fromstring(self._schema)

            tree_values = tree.findall(
                './/{{http://www.w3.org/2001/XMLSchema}}simpleType['
                '@name="{}"]/'
                '{{http://www.w3.org/2001/XMLSchema}}restriction/'
                '{{http://www.w3.org/2001/XMLSchema}}enumeration'.format(
                    self.typename))

            for e in tree_values:
                code = self._typeconvert(
                    e.get('value'), self.datatype)
                label = e.findtext(
                    './{http://www.w3.org/2001/XMLSchema}annotation/{'
                    'http://www.w3.org/2001/XMLSchema}documentation')
                yield CodeListItem(code, label)

    def resolve(self):
        self._schema = self.get_remote_codelist()
        self.items = list(self._get_xsd_enum_values())

    def get_values(self):
        self.resolve()
        return super().get_values()
