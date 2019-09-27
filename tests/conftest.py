"""Module grouping session scoped PyTest fixtures."""

import pytest
from _pytest.monkeypatch import MonkeyPatch

import pydov


def pytest_runtest_setup():
    pydov.hooks = []

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "online: mark test that requires internet access")

@pytest.fixture(scope='module')
def monkeymodule():
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()
