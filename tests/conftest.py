"""Module grouping session scoped PyTest fixtures."""

import pytest
from _pytest.monkeypatch import MonkeyPatch

import pydov


def pytest_runtest_setup():
    pydov.hooks = []


@pytest.fixture(scope='module')
def monkeymodule():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
