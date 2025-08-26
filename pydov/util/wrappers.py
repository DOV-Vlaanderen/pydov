"""Module with a class that provides a dictionary-like interface with attribute access."""


class AbstractDictLike:
    """A class that provides a dictionary-like interface with attribute access."""

    def __init__(self, base_dict=None):
        """Initialisation.

        Parameters
        ----------
        base_dict : dict, optional
            The base dictionary to wrap. Defaults to None, which means an empty
            dictionary is used.

        Raises
        ------
        TypeError
            If base_dict is not a dictionary.
        """
        if base_dict is None:
            base_dict = dict()

        if not isinstance(base_dict, dict):
            raise TypeError('base_dict should be a dictionary')

        self.base_dict = base_dict

    def __dir__(self):
        """List the keys of the dictionary as attributes.

        Returns
        -------
        attributes : list of str
            The keys of the dictionary as attributes.
        """
        return list(self.base_dict.keys())

    def __contains__(self, name):
        """Check if a key is in the dictionary.

        Parameters
        ----------
        name : str
            The key to check.

        Returns
        -------
        bool
            Whether the key is in the dictionary.
        """
        return name in self.base_dict

    def __iter__(self):
        """Iterate over the keys of the dictionary.

        Yields
        ------
        key : str
            The next key in the dictionary.
        """
        for item in self.base_dict:
            yield item

    def __next__(self):
        """Get the next key in the dictionary.

        Returns
        -------
        key : str
            The next key in the dictionary.
        """
        return next(self.base_dict)

    def __getitem__(self, name):
        """Get an item from the dictionary.

        Parameters
        ----------
        name : str
            The key to get.

        Returns
        -------
        value : object
            The value associated with the key.
        """
        if name in self.base_dict:
            return self.base_dict.get(name)
        raise KeyError(f'{name}')

    def __getattr__(self, name):
        """Get an attribute from the dictionary.

        Parameters
        ----------
        name : str
            The attribute to get.

        Returns
        -------
        value : object
            The value associated with the attribute.
        """
        if name in self.base_dict:
            return self.base_dict.get(name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has not attribute '{name}'")

    def __len__(self):
        """Get the number of items in the dictionary.

        Returns
        -------
        length : int
            The number of items in the dictionary.
        """
        return len(self.base_dict)

    def __repr__(self):
        """String representation of the dictionary.

        Returns
        -------
        str
            String representation of the dictionary.
        """
        return self.base_dict.__repr__()

    def keys(self):
        """Get the keys of the dictionary.

        Returns
        -------
        keys : list of str
            The keys of the dictionary.
        """
        return self.base_dict.keys()

    def values(self):
        """Get the values of the dictionary.

        Returns
        -------
        values : list of object
            The values of the dictionary.
        """
        return self.base_dict.values()
