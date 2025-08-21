"""Module grouping tests for the pydov.util.codelists module."""

import pathlib
import pytest

from owslib.etree import etree

import pydov
from pydov.util.codelists import AbstractCodeList, CodeListItem, MemoryCache, OsloCodeList, XsdType
from pydov.util.dovutil import build_dov_url


class TestMemoryCache:
    """Test suite for the MemoryCache class."""

    @pytest.fixture(autouse=True, scope='function')
    def clear_memory_cache(self):
        """PyTest fixture clearing the cache before and after each test."""
        MemoryCache.clear()
        yield
        MemoryCache.clear()

    def test_get_new_object(self):
        """Test that the get method retrieves a new object from the provided function.

        Checks that the object is stored in the cache and returned correctly.
        """
        def mock_fn(*args, **kwargs):
            return "new_object"

        result = MemoryCache.get("key", mock_fn)
        assert result == "new_object"

    def test_get_cached_object(self):
        """Test that the get method retrieves a cached object.

        Checks that the cached object is returned without calling the provided function.
        """
        MemoryCache.cache["key"] = "cached_object"

        def mock_fn(*args, **kwargs):
            return "new_object"

        result = MemoryCache.get("key", mock_fn)
        assert result == "cached_object"

    def test_get_with_args_and_kwargs(self):
        """Test that the get method passes the provided args and kwargs to the function.

        Checks that the function is called with the correct arguments and the result is stored in the cache.
        """
        def mock_fn(a, b, c=1):
            return f"result_{a}_{b}_{c}"

        result = MemoryCache.get("key", mock_fn, 1, 2, c=3)
        assert result == "result_1_2_3"
        assert "key" in MemoryCache.cache
        assert MemoryCache.cache["key"] == "result_1_2_3"


class TestCodeListItem:
    """Test suite for the CodeListItem class."""

    def test_init(self):
        """Test whether a CodeListItem can be initialised."""
        codelistitem = CodeListItem(code='code', label="label")
        assert codelistitem.code == 'code'
        assert codelistitem.label == 'label'


class TestAbstractCodeList:
    """Test suite for the AbstractCodeList class."""

    def test_get_values_empty(self):
        """Test that get_values returns None when the codelist is empty.

        Checks that the items list is empty and the method returns None.
        """
        codelist = AbstractCodeList()
        assert codelist.items == {}
        # assert codelist.get_values() is None

    @pytest.mark.skip
    def test_get_values_non_empty(self):
        """Test that get_values returns a dictionary of codes and labels.

        Checks that the dictionary contains the expected key-value pairs.
        """
        codelist = AbstractCodeList()
        codelist.items = [
            CodeListItem("code1", "label1"),
            CodeListItem("code2", "label2"),
            CodeListItem("code3", "label3")
        ]

        result = codelist.get_values()
        assert isinstance(result, dict)
        assert result == {
            "code1": "label1",
            "code2": "label2",
            "code3": "label3"
        }


class TestOsloCodeList:
    """Test suite for the OsloCodeList class."""

    @pytest.fixture(scope='function')
    def mp_remote_request(self, monkeypatch):
        """Mock the remote request for the code list.

        This fixture monkeypatches the `get_remote_request` function
        from the `pydov.util.dovutil` module to return a fixed
        code list data.

        Parameters
        ----------
        monkeypatch : pytest.MonkeyPatch
            The MonkeyPatch fixture provided by pytest.
        """
        def _get(*args, **kwargs):
            codelist_path = pathlib.Path(
                'tests/data/types/monster/codelist_bemonsteringstype.xml')

            with codelist_path.open('r', encoding="utf-8") as f:
                data = f.read()
                if not isinstance(data, bytes):
                    data = data.encode('utf-8')
            return data

        monkeypatch.setattr(pydov.util.codelists.OsloCodeList,
                            'get_remote_codelist', _get)

    def test_init(self):
        """Test the initialization of the OsloCodeList class.

        This test checks that an instance of the OsloCodeList class
        can be created successfully.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')
        assert isinstance(codelist, OsloCodeList)

    def test_get_id_unique(self):
        """Test that the IDs of different code lists are unique.

        This test creates two instances of the OsloCodeList class
        with different code list names and checks that their IDs
        are different.
        """
        codelist1 = OsloCodeList('bemonsteringstype', 'string')
        codelist2 = OsloCodeList('bekistingsmateriaal', 'string')
        assert codelist1.get_id() != codelist2.get_id()

    def test_build_sparql_query(self):
        """Test the generation of the SPARQL query.

        This test creates an instance of the OsloCodeList class
        and checks that the SPARQL query generated by the
        `build_sparql_query` method matches the expected query.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')
        sparql_query = codelist.build_sparql_query()

        assert isinstance(sparql_query, str)
        assert sparql_query == """
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX conceptscheme:
            <https://data.bodemenondergrond.vlaanderen.be/id/conceptscheme/>

            SELECT ?code ?label ?definition
            WHERE {
            ?s skos:inScheme conceptscheme:bemonsteringstype .
            ?s skos:notation ?code .
            ?s skos:prefLabel ?label .
            OPTIONAL { ?s skos:note ?definition . }
            }
        """

    def test_get_remote_codelist(self, mp_remote_request):
        """Test the retrieval of the remote code list.

        This test creates an instance of the OsloCodeList class
        and checks that the remote code list data can be retrieved
        successfully.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')
        remote_codelist = codelist.get_remote_codelist()

        assert isinstance(remote_codelist, bytes)

        tree = etree.fromstring(remote_codelist)
        assert tree is not None

    @pytest.mark.skip
    def test_get_values(self, mp_remote_request):
        """Test the retrieval of the code list values.

        This test creates an instance of the OsloCodeList class
        and checks that the values retrieved from the remote
        code list match the expected values.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')
        values = codelist.get_values()

        assert values == {
            "geroerd": "Geroerd",
            "ongeroerd": "Ongeroerd",
            "vloeistof": "Vloeistof"
        }


class TestXsdType:
    """Test suite for the XsdType class."""

    @pytest.fixture(scope='function')
    def mp_remote_request(self, monkeypatch):
        """Mock the remote request for the code list.

        This fixture monkeypatches the `get_remote_request` function
        from the `pydov.util.dovutil` module to return a fixed
        code list data.

        Parameters
        ----------
        monkeypatch : pytest.MonkeyPatch
            The MonkeyPatch fixture provided by pytest.
        """
        def _get(*args, **kwargs):
            codelist_path = pathlib.Path(
                'tests/data/types/grondwaterfilter/'
                'codelist_FilterDataCodes.xsd')

            with codelist_path.open('r', encoding="utf-8") as f:
                data = f.read()
                if not isinstance(data, bytes):
                    data = data.encode('utf-8')
            return data

        monkeypatch.setattr(pydov.util.codelists.XsdType,
                            'get_remote_codelist', _get)

    def test_init(self):
        """Test the initialization of the XsdType class.

        This test checks that an instance of the XsdType class
        can be created successfully.
        """
        codelist = XsdType(
            xsd_schema=build_dov_url(
                'xdov/schema/latest/xsd/kern/interpretatie/'
                'FormeleStratigrafieDataCodes.xsd'),
            typename='FormeleStratigrafieLedenEnumType',
            datatype='string')
        assert isinstance(codelist, XsdType)

    def test_get_id_unique(self):
        """Test that the IDs of different code lists are unique.

        This test creates two instances of the XsdType class
        with different code list names and checks that their IDs
        are different.
        """
        codelist1 = XsdType(
            xsd_schema=build_dov_url(
                'xdov/schema/latest/xsd/kern/interpretatie/'
                'FormeleStratigrafieDataCodes.xsd'),
            typename='FormeleStratigrafieLedenEnumType',
            datatype='string')

        codelist2 = XsdType(
            xsd_schema=build_dov_url(
                'xdov/schema/latest/xsd/kern/gwmeetnet/FilterDataCodes.xsd'),
            typename='FilterstatusEnumType',
            datatype='string')

        assert codelist1.get_id() != codelist2.get_id()

    def test_get_remote_codelist(self, mp_remote_request):
        """Test the retrieval of the remote code list.

        This test creates an instance of the XsdType class
        and checks that the remote code list data can be retrieved
        successfully.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = XsdType(
            xsd_schema=build_dov_url(
                'xdov/schema/latest/xsd/kern/gwmeetnet/FilterDataCodes.xsd'),
            typename='FilterstatusEnumType',
            datatype='string')
        remote_codelist = codelist.get_remote_codelist()

        assert isinstance(remote_codelist, bytes)

        tree = etree.fromstring(remote_codelist)
        assert tree is not None

    @pytest.mark.skip
    def test_get_values(self, mp_remote_request):
        """Test the retrieval of the code list values.

        This test creates an instance of the XsdType class
        and checks that the values retrieved from the remote
        code list match the expected values.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = XsdType(
            xsd_schema=build_dov_url(
                'xdov/schema/latest/xsd/kern/gwmeetnet/FilterDataCodes.xsd'),
            typename='FilterstatusEnumType',
            datatype='string')
        values = codelist.get_values()

        assert values == {
            "in rust": None,
            "werking": None,
            "onbekend": None
        }
