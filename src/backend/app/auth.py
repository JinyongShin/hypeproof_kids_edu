"""
Admin authentication helpers.
DB admins table is checked first; env-var fallback preserves pilot day backwards compat.
"""

import asyncio
import logging

import bcrypt

logger = logging.getLogger(__name__)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


async def authenticate(username: str, password: str) -> dict | None:
    """
    Returns {"admin_id": ..., "tenant_id": ..., "role": ...} on success, None on failure.
    DB lookup first; plain-text env-var fallback for pilot compatibility.
    """
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    import storage

    # DB path for async thread
    row = await asyncio.to_thread(storage.get_admin_by_email, username)
    if row is not None:
        if await asyncio.to_thread(verify_password, password, row["pw_hash"]):
            return {
                "admin_id": row["admin_id"],
                "tenant_id": row["tenant_id"],
                "role": row["role"],
            }
        return None

    # Env-var fallback (파일럿 당일 하드코딩 root/0000 호환)
    from app.config import get_settings
    s = get_settings()
    if username == s.ADMIN_USERNAME and password == s.ADMIN_PASSWORD:
        return {"admin_id": username, "tenant_id": "default", "role": "admin"}

    return None


async def ensure_default_admin() -> None:
    """서버 시작 시 1회 호출. DB에 admin이 없을 때만 env-var 값으로 시딩."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    import storage

    from app.config import get_settings
    s = get_settings()

    # ADMIN_USERNAME이 기본값이면 시딩 생략 (파일럿 env-var 전용 모드)
    if not s.ADMIN_USERNAME or s.ADMIN_USERNAME in ("admin", "root"):
        logger.info("ensure_default_admin: env-var 전용 모드, DB 시딩 생략")
        return

    pw_hash = await asyncio.to_thread(hash_password, s.ADMIN_PASSWORD)
    await asyncio.to_thread(storage.seed_default_admin, s.ADMIN_USERNAME, pw_hash)
