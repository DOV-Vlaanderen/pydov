"""Module grouping session scoped PyTest fixtures."""

import pytest
from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(scope='session')
def monkeysession():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
