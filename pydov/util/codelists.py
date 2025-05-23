import warnings
from pydov.search.abstract import AbstractCommon
from pydov.util.dovutil import get_remote_url
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

    def resolve(self):
        raise NotImplementedError


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

        self.xsd_schema = xsd_schema
        self.typename = typename

        self._schema = None

    def _get_xsd_schema(self):
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
        response = HookRunner.execute_inject_meta_response(self.xsd_schema)

        if response is None:
            try:
                response = MemoryCache.get(
                    self.xsd_schema, get_remote_url, self.xsd_schema)
            except RemoteFetchError:
                warnings.warn(
                    "Failed to fetch remote XSD schema, metadata will "
                    "be incomplete.", XsdFetchWarning)
                response = None

        HookRunner.execute_meta_received(self.xsd_schema, response)

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
        self._schema = self._get_xsd_schema()
        self.items = list(self._get_xsd_enum_values())

    def get_values(self):
        self.resolve()
        return super().get_values()
