import pytest
import sys

from pydov.util.deprecation import DeprecatedModule


class TestDeprecatedModule:
    """Test the DeprecatedModule class."""

    def test_init(self):
        """Test that the module is correctly initialised and added to sys.modules."""
        module_name = "deprecated_test_module"
        message = "This is a deprecated module: {name}"
        deprecated_module = DeprecatedModule(module_name, message)

        assert module_name in sys.modules
        assert sys.modules[module_name] is deprecated_module
        assert deprecated_module._name == module_name
        assert deprecated_module._message == message

        # Clean up sys.modules
        del sys.modules[module_name]

    def test_getattr_raises_modulenotfounderror(self):
        """Test that accessing any attribute raises ModuleNotFoundError."""
        module_name = "another_deprecated_module"
        message = 'The module "{name}" is no longer supported.'
        deprecated_module = DeprecatedModule(module_name, message)

        expected_message = message.format(name=module_name)

        with pytest.raises(ModuleNotFoundError) as excinfo:
            deprecated_module.some_attribute

        assert str(excinfo.value) == expected_message

        with pytest.raises(ModuleNotFoundError) as excinfo:
            deprecated_module.some_method()

        assert str(excinfo.value) == expected_message

        # Clean up sys.modules
        del sys.modules[module_name]

    def test_dir_returns_empty_list(self):
        """Test that __dir__ returns an empty list."""
        module_name = "not_inspectable_module"
        message = "Do not inspect {name}."
        deprecated_module = DeprecatedModule(module_name, message)

        assert deprecated_module.__dir__() == []
        assert dir(deprecated_module) == []

        # Clean up sys.modules
        del sys.modules[module_name]

    def test_module_in_sys_modules_behaves_correctly(self):
        """Test that accessing the module through sys.modules raises the error."""
        module_name = "sys_deprecated_module"
        message = "Accessing {name} is forbidden."
        DeprecatedModule(module_name, message)  # This registers it in sys.modules

        with pytest.raises(ModuleNotFoundError) as excinfo:
            sys.modules[module_name].a_function()

        expected_message = message.format(name=module_name)
        assert str(excinfo.value) == expected_message

        # Clean up sys.modules
        del sys.modules[module_name]
