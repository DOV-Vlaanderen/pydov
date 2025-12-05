from pydov.util.deprecation import DeprecatedModule

_monster_search = (
    "The '{name}' module has been deprecated and removed in pydov 4.\n"
    "Please update your code to use the new generic Monster search: "
    "pydov.search.monster\n"
    "Check the documentation for more information: "
    "https://pydov.readthedocs.io/en/stable/history.html#v4-0-0"
)

DeprecatedModule("pydov.search.grondmonster", _monster_search)
DeprecatedModule("pydov.search.grondwatermonster", _monster_search)
DeprecatedModule("pydov.search.bodemmonster", _monster_search)

_observatie_search = (
    "The '{name}' module has been deprecated and removed in pydov 4.\n"
    "Please update your code to use the new generic Observatie search: "
    "pydov.search.observatie\n"
    "Check the documentation for more information: "
    "https://pydov.readthedocs.io/en/stable/history.html#v4-0-0"
)

DeprecatedModule("pydov.search.bodemobservatie", _observatie_search)
