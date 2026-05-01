"""
Unit tests for app/auth.py — password hashing + authenticate() flow.
DB isolation via storage._DB_PATH monkey-patch with tmp_path fixture.
"""

import os
import pytest


# ---------------------------------------------------------------------------
# hash_password / verify_password
# ---------------------------------------------------------------------------

def test_hash_and_verify():
    from app.auth import hash_password, verify_password
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_verify_invalid_hash_returns_false():
    from app.auth import verify_password
    assert not verify_password("any", "not-a-valid-hash")


# ---------------------------------------------------------------------------
# authenticate() — DB path
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_authenticate_db_admin(tmp_path):
    import storage
    from app.auth import authenticate, hash_password

    pw_hash = hash_password("pw1234")
    storage.seed_default_admin("admin@test.com", pw_hash)

    result = await authenticate("admin@test.com", "pw1234")
    assert result is not None
    assert result["tenant_id"] == "default"
    assert result["role"] == "root"


@pytest.mark.asyncio
async def test_authenticate_db_wrong_password():
    import storage
    from app.auth import authenticate, hash_password

    storage.seed_default_admin("admin@test.com", hash_password("correct"))

    result = await authenticate("admin@test.com", "wrong")
    assert result is None


# ---------------------------------------------------------------------------
# authenticate() — env-var fallback
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_authenticate_env_fallback(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "envuser")
    monkeypatch.setenv("ADMIN_PASSWORD", "envpass")

    # lru_cache 무효화
    from app import config
    config.get_settings.cache_clear()

    from app.auth import authenticate
    result = await authenticate("envuser", "envpass")
    assert result is not None
    assert result["tenant_id"] == "default"

    config.get_settings.cache_clear()


@pytest.mark.asyncio
async def test_authenticate_env_fallback_wrong(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "envuser")
    monkeypatch.setenv("ADMIN_PASSWORD", "envpass")

    from app import config
    config.get_settings.cache_clear()

    from app.auth import authenticate
    result = await authenticate("envuser", "wrongpass")
    assert result is None

    config.get_settings.cache_clear()


@pytest.mark.asyncio
async def test_authenticate_unknown_user_returns_none(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "root")
    monkeypatch.setenv("ADMIN_PASSWORD", "0000")

    from app import config
    config.get_settings.cache_clear()

    from app.auth import authenticate
    result = await authenticate("nobody@test.com", "anything")
    assert result is None

    config.get_settings.cache_clear()
