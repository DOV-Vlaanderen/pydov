"""Module grouping session scoped PyTest fixtures."""

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(scope='module')
def monkeymodule():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
