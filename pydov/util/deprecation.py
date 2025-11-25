import sys


class DeprecatedModule:
    """A placeholder module that raises a ModuleNotFoundError upon
    attribute access.

    This class is used to replace deprecated modules. When an attempt is
    made to access any attribute of a deprecated module, a
    ModuleNotFoundError is raised with a custom message.

    Parameters
    ----------
    name : str
        The name of the deprecated module.
    message : str
        The deprecation message to be displayed when the module is
        accessed. This message should contain the placeholder ``{name}``
        which will be replaced by the module's name.

    """

    def __init__(self, name, message):
        """Initialise the DeprecatedModule.

        Parameters
        ----------
        name : str
            The name of the deprecated module.
        message : str
            The deprecation message to be displayed when the module is
            accessed. This message should contain the placeholder ``{name}``
            which will be replaced by the module's name.

        """
        self._name = name
        self._message = message

        sys.modules[name] = self

    def __getattr__(self, item):
        """Raise a ModuleNotFoundError when any attribute is accessed.

        Parameters
        ----------
        item : str
            The name of the attribute being accessed (ignored).

        Raises
        ------
        ModuleNotFoundError
            Always raises this error with the custom deprecation message.

        """
        raise ModuleNotFoundError(self._message.format(name=self._name))

    def __dir__(self):
        """Prevent introspection from revealing non-existent attributes.

        Returns
        -------
        list
            An empty list, indicating no accessible attributes.

        """
        # Prevent introspection from revealing non-existent attributes
        return []
