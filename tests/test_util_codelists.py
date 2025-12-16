"""Module grouping tests for the pydov.util.codelists module."""

import pathlib
import pytest

from owslib.etree import etree

import pydov
from pydov.util.codelists import AbstractCodeList, CodeListItem, FeatureCatalogueValues, MemoryCache, OsloCodeList, XsdType
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

    def test_init_with_definition(self):
        """Test whether a CodeListItem can be initialised with a definition."""
        codelistitem = CodeListItem(code='code', label="label",
                                    definition="definition")
        assert codelistitem.code == 'code'
        assert codelistitem.label == 'label'
        assert codelistitem.definition == 'definition'


class TestAbstractCodeList:
    """Test suite for the AbstractCodeList class."""

    @pytest.fixture
    def codelist(self):
        """Fixture providing an instance of the AbstractCodeList class."""
        codelist = AbstractCodeList()
        codelist.add_items([
            CodeListItem("code1", "label1", "definition1"),
            CodeListItem("code2", "label2", "definition2"),
            CodeListItem("code3", "label3", "definition3")
        ])
        yield codelist

    def test_get_values_empty(self):
        """Test that get_values returns None when the codelist is empty.

        Checks that the items list is empty and the method returns None.
        """
        codelist = AbstractCodeList()
        assert codelist.items == {}
        assert codelist.get_values() is None

    def test_get_values_non_empty(self, codelist):
        """Test that get_values returns a dictionary of codes and labels.

        Checks that the dictionary contains the expected key-value pairs.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        result = codelist.get_values()
        assert isinstance(result, dict)
        assert result == {
            "code1": "label1",
            "code2": "label2",
            "code3": "label3"
        }

    def test_get_label(self, codelist):
        """Test that get_label returns the correct label for a given code.

        Checks that the method returns the expected label for existing codes
        and None for non-existing codes.
        
        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        assert codelist.get_label("code1") == "label1"
        assert codelist.get_label("code2") == "label2"
        assert codelist.get_label("code3") == "label3"
        assert codelist.get_label("non_existing_code") is None

    def test_get_definition(self, codelist):
        """Test that get_definition returns the correct definition for a given code.

        Checks that the method returns the expected definition for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        assert codelist.get_definition("code1") == "definition1"
        assert codelist.get_definition("code2") == "definition2"
        assert codelist.get_definition("code3") == "definition3"
        assert codelist.get_definition("non_existing_code") is None

    def test_get_codelist(self, codelist):
        """Test that get_codelist returns the codelist itself.

        Checks that the returned object is the same as the original codelist.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        result = codelist.get_codelist()
        assert result is codelist

    def test_get(self, codelist):
        """Test that get retrieves the correct CodeListItem for a given code.

        Checks that the method returns the expected CodeListItem for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        item1 = codelist.get("code1")
        assert isinstance(item1, CodeListItem)
        assert item1.code == "code1"
        assert item1.label == "label1"
        assert item1.definition == "definition1"

        assert codelist.get("non_existing_code") is None
        assert codelist.get("non_existing_code", 'default') is 'default'

    def test_add_item(self):
        """Test that add_item adds a CodeListItem to the codelist.

        Checks that the item is added correctly and can be retrieved.
        """
        codelist = AbstractCodeList()
        item = CodeListItem("code1", "label1", "definition1")
        codelist.add_item(item)

        assert "code1" in codelist.items
        assert codelist.items["code1"] is item

    def test_add_items(self):
        """Test that add_items adds multiple CodeListItems to the codelist.

        Checks that all items are added correctly and can be retrieved.
        """
        codelist = AbstractCodeList()
        items = [
            CodeListItem("code1", "label1", "definition1"),
            CodeListItem("code2", "label2", "definition2"),
            CodeListItem("code3", "label3", "definition3")
        ]
        codelist.add_items(items)

        for item in items:
            assert item.code in codelist.items
            assert codelist.items[item.code] is item

    def test_is_empty(self):
        """Test that is_empty returns True for an empty codelist and False otherwise."""
        codelist = AbstractCodeList()
        assert codelist.is_empty() is True

        item = CodeListItem("code1", "label1", "definition1")
        codelist.add_item(item)
        assert codelist.is_empty() is False

    def test_get_item(self, codelist):
        """Test that get retrieves the correct CodeListItem for a given code.

        Checks that the method returns the expected CodeListItem for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        item1 = codelist['code1']
        assert isinstance(item1, CodeListItem)
        assert item1.code == "code1"
        assert item1.label == "label1"
        assert item1.definition == "definition1"

        with pytest.raises(KeyError):
            codelist["non_existing_code"]

    def test_get_attr(self, codelist):
        """Test that __getattr__ retrieves the correct CodeListItem for a given code.

        Checks that the method returns the expected CodeListItem for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        item1 = codelist.code1
        assert isinstance(item1, CodeListItem)
        assert item1.code == "code1"
        assert item1.label == "label1"
        assert item1.definition == "definition1"

        with pytest.raises(AttributeError):
            codelist.non_existing_code

    def test_iter(self, codelist):
        """Test that __iter__ iterates over the CodeListItems in the codelist.

        Checks that all items are returned in the iteration.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        codes = set()
        for code in codelist:
            assert isinstance(code, str)

            item = codelist.get(code)
            assert isinstance(item, CodeListItem)

            codes.add(item.code)

        assert codes == {"code1", "code2", "code3"}

    def test_len(self, codelist):
        """Test that __len__ returns the correct number of items in the codelist.

        Parameters
        ----------
        codelist : AbstractCodeList
            An instance of the AbstractCodeList class with items.
        """
        assert len(codelist) == 3

        codelist.add_item(CodeListItem("code4", "label4", "definition4"))
        assert len(codelist) == 4


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

    def test_get_label(self, mp_remote_request):
        """Test that get_label returns the correct label for a given code.

        Checks that the method returns the expected label for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')

        assert codelist.get_label("geroerd") == "Geroerd"
        assert codelist.get_label("ongeroerd") == "Ongeroerd"
        assert codelist.get_label("vloeistof") == "Vloeistof"
        assert codelist.get_label("non_existing_code") is None

    def test_get_definition(self, mp_remote_request):
        """Test that get_definition returns the correct definition for a given code.

        Checks that the method returns the expected definition for existing codes
        and None for non-existing codes.

        Parameters
        ----------
        mp_remote_request : fixture
            The `mp_remote_request` fixture, which mocks the
            remote request for the code list.
        """
        codelist = OsloCodeList('bemonsteringstype', 'string')

        assert codelist.get_definition("geroerd") == \
            ("Monstername waarbij de oorspronkelijke structuur en gelaagdheid "
             "van het materiaal niet bewaard wordt. Het resulterende monster "
             "laat het niet toe een gedetailleerde beschrijving of bepaalde "
             "analyses met betrekking tot de structuur of gelaagdheid  (bv. "
             "Bulkdensiteit, volumemassa, grondmechanische proeven, ....) uit "
             "te voeren.")

        assert codelist.get_definition("ongeroerd") is not None
        assert codelist.get_definition("vloeistof") is not None
        assert codelist.get_definition("non_existing_code") is None


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
            "in rust": "in rust",
            "werking": "werking",
            "onbekend": "onbekend"
        }

    def test_get_label(self, mp_remote_request):
        """Test that get_label returns the correct label for a given code.

        Checks that the method returns the expected label for existing codes
        and None for non-existing codes.

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

        assert codelist.get_label("in rust") == "in rust"
        assert codelist.get_label("werking") == "werking"
        assert codelist.get_label("onbekend") == "onbekend"
        assert codelist.get_label("non_existing_code") is None

    def test_get_definition(self, mp_remote_request):
        """Test that get_definition returns the correct definition for a given code.

        Checks that the method returns the expected definition for existing codes
        and None for non-existing codes.

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

        assert codelist.get_definition("in rust") is None
        assert codelist.get_definition("werking") is None
        assert codelist.get_definition("onbekend") is None
        assert codelist.get_definition("non_existing_code") is None


class TestFeatureCatalogueValues:
    """Test suite for the FeatureCatalogueValues class."""

    def test_init(self):
        """Test the initialization of the FeatureCatalogueValues class.

        This test checks that an instance of the FeatureCatalogueValues class
        can be created successfully.
        """
        codelist = FeatureCatalogueValues()
        assert isinstance(codelist, FeatureCatalogueValues)
        assert isinstance(codelist, AbstractCodeList)
