from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(config, items):
    """Keep platform-specific suites explicit and honest on native Windows."""
    del config
    if os.name == "nt":
        skip_posix = pytest.mark.skip(
            reason="posix_only: run this test group in WSL/Linux"
        )
        for item in items:
            if item.get_closest_marker("posix_only"):
                item.add_marker(skip_posix)
    else:
        skip_windows = pytest.mark.skip(
            reason="windows_only: run this test group on native Windows"
        )
        for item in items:
            if item.get_closest_marker("windows_only"):
                item.add_marker(skip_windows)
