from pydov.util.deprecation import DeprecatedModule

_monster_types = (
    "The '{name}' module has been deprecated and removed in pydov 4.\n"
    "Please update your code to use the new generic Monster types: "
    "pydov.types.monster\n"
    "Check the documentation for more information: "
    "https://pydov.readthedocs.io/en/stable/history.html#v4-0-0"
)

DeprecatedModule("pydov.types.grondmonster", _monster_types)
DeprecatedModule("pydov.types.grondwatermonster", _monster_types)
