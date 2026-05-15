"""
Shared test fixtures.
Sets up an isolated SQLite DB for each test so storage calls in nodes don't
hit a missing-table error or the live data directory.
"""

import pytest


@pytest.fixture(autouse=True)
def isolate_storage_db(tmp_path, monkeypatch):
    """Redirect storage._DB_PATH to a fresh temp DB for every test."""
    import storage
    monkeypatch.setattr(storage, "_DB_PATH", tmp_path / "test.db")
    storage.init_db()
