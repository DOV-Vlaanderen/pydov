"""Class grouping tests for the pydov.util.wrappers module."""

import pytest

from pydov.util.wrappers import AbstractDictLike


class TestAbstractDictLike:
    """Class grouping tests for the AbstractDictLike class."""

    @pytest.fixture
    def base_dict(self):
        """Fixture returning a base dictionary for testing."""
        return {'key1': 'value1', 'key2': 'value2'}

    def test_initialise(self, base_dict):
        """Test initialisation of AbstractDictLike."""
        adl = AbstractDictLike(base_dict)
        assert isinstance(adl, AbstractDictLike)

    def test_dir(self, base_dict):
        """Test the __dir__ method."""
        adl = AbstractDictLike(base_dict)
        attributes = dir(adl)
        for key in base_dict.keys():
            assert key in attributes

    def test_contains(self, base_dict):
        """Test the __contains__ method."""
        adl = AbstractDictLike(base_dict)
        for key in base_dict.keys():
            assert key in adl
        assert 'nonexistent_key' not in adl

    def test_iter(self, base_dict):
        """Test the __iter__ method."""
        adl = AbstractDictLike(base_dict)
        keys = list(iter(adl))
        assert keys == list(base_dict.keys())

    def test_next(self, base_dict):
        """Test the __next__ method."""
        adl = AbstractDictLike(base_dict)
        iterator = iter(adl)
        keys = []
        try:
            while True:
                keys.append(next(iterator))
        except StopIteration:
            pass
        assert keys == list(base_dict.keys())

    def test_getitem(self, base_dict):
        """Test the __getitem__ method."""
        adl = AbstractDictLike(base_dict)
        for key, value in base_dict.items():
            assert adl[key] == value

        with pytest.raises(KeyError):
            _ = adl['nonexistent_key']

    def test_getattr(self, base_dict):
        """Test the __getattr__ method."""
        adl = AbstractDictLike(base_dict)
        for key, value in base_dict.items():
            assert getattr(adl, key) == value

        with pytest.raises(AttributeError):
            _ = adl.nonexistent_key

    def test_keys(self, base_dict):
        """Test the keys method."""
        adl = AbstractDictLike(base_dict)
        keys = adl.keys()
        assert list(keys) == list(base_dict.keys())

    def test_values(self, base_dict):
        """Test the values method."""
        adl = AbstractDictLike(base_dict)
        values = adl.values()
        assert list(values) == list(base_dict.values())

    def test_len(self, base_dict):
        """Test the __len__ method."""
        adl = AbstractDictLike(base_dict)
        assert len(adl) == len(base_dict)
