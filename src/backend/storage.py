"""
SQLite storage layer for Kids Edu Backend.
All functions are synchronous (sqlite3 standard library).
Use asyncio.to_thread(...) when calling from async context.
"""

import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).parent
_DB_PATH = _BACKEND_ROOT / "data" / "kids_edu.db"

_DDL = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id        TEXT PRIMARY KEY,
    child_id          TEXT NOT NULL,
    name              TEXT NOT NULL DEFAULT '',
    created_at        TEXT NOT NULL,
    claude_session_id TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL,
    child_id    TEXT NOT NULL,
    role        TEXT NOT NULL CHECK(role IN ('user','assistant')),
    content     TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS games (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL,
    child_id    TEXT NOT NULL,
    game_id     TEXT NOT NULL,
    file_path   TEXT NOT NULL,
    url         TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS cards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL,
    child_id    TEXT NOT NULL,
    card_id     TEXT NOT NULL,
    card_type   TEXT NOT NULL CHECK(card_type IN ('character','world','title')),
    card_json   TEXT NOT NULL,
    url         TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts
    USING fts5(content, content='messages', content_rowid='id');

CREATE TRIGGER IF NOT EXISTS messages_fts_ai
    AFTER INSERT ON messages BEGIN
        INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
    END;
"""


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """DB/테이블 생성. 서버 구동 시 1회 호출."""
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.executescript(_DDL)
    logger.info("SQLite DB 초기화 완료: %s", _DB_PATH)


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

def create_session(session_id: str, child_id: str, name: str, created_at: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO sessions (session_id, child_id, name, created_at) VALUES (?,?,?,?)",
            (session_id, child_id, name, created_at),
        )


def list_sessions(child_id: str) -> list[dict]:
    """child_id의 세션 목록. last_game_url은 games 테이블 MAX subquery."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT
                s.session_id,
                s.child_id,
                s.name,
                s.created_at,
                COALESCE(
                    (SELECT g.url FROM games g
                     WHERE g.session_id = s.session_id
                     ORDER BY g.created_at DESC LIMIT 1),
                    ''
                ) AS last_game_url
            FROM sessions s
            WHERE s.child_id = ?
            ORDER BY s.created_at ASC
            """,
            (child_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def update_session_name(session_id: str, name: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE sessions SET name=? WHERE session_id=?",
            (name, session_id),
        )


def get_claude_session_id(session_id: str):
    with _connect() as conn:
        row = conn.execute(
            "SELECT claude_session_id FROM sessions WHERE session_id=?",
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    val = row["claude_session_id"]
    return val if val else None


def set_claude_session_id(session_id: str, claude_sid: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE sessions SET claude_session_id=? WHERE session_id=?",
            (claude_sid, session_id),
        )


def delete_claude_session_id(session_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE sessions SET claude_session_id='' WHERE session_id=?",
            (session_id,),
        )


def delete_session(session_id: str) -> None:
    """sessions + messages + games 모두 삭제 (단일 트랜잭션)."""
    conn = _connect()
    try:
        conn.execute("BEGIN")
        conn.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
        conn.execute("DELETE FROM games    WHERE session_id=?", (session_id,))
        conn.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

def append_message(session_id: str, child_id: str, role: str, content: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, child_id, role, content) VALUES (?,?,?,?)",
            (session_id, child_id, role, content),
        )


def load_messages(session_id: str) -> list[dict]:
    """[{"role": ..., "text": ...}] 형식으로 반환."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM messages WHERE session_id=? ORDER BY id ASC",
            (session_id,),
        ).fetchall()
    return [{"role": r["role"], "text": r["content"]} for r in rows]


def message_count(session_id: str) -> int:
    with _connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM messages WHERE session_id=?",
            (session_id,),
        ).fetchone()
    return row["cnt"] if row else 0


# ---------------------------------------------------------------------------
# Games
# ---------------------------------------------------------------------------

def add_game(session_id: str, child_id: str, game_id: str, file_path: str, url: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO games (session_id, child_id, game_id, file_path, url) VALUES (?,?,?,?,?)",
            (session_id, child_id, game_id, file_path, url),
        )


def list_games(session_id: str) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT game_id, file_path, url, created_at FROM games WHERE session_id=? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_latest_game_url(session_id: str) -> str:
    with _connect() as conn:
        row = conn.execute(
            "SELECT url FROM games WHERE session_id=? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        ).fetchone()
    return row["url"] if row else ""


def delete_game(session_id: str, game_id: str) -> None:
    """게임 레코드 삭제 (파일시스템 파일 삭제는 호출자 책임)."""
    with _connect() as conn:
        conn.execute(
            "DELETE FROM games WHERE session_id=? AND game_id=?",
            (session_id, game_id),
        )


def reset_all_claude_sessions(child_id: str) -> int:
    """child_id의 모든 세션에서 claude_session_id를 초기화. 변경된 행 수 반환."""
    with _connect() as conn:
        result = conn.execute(
            "UPDATE sessions SET claude_session_id='' WHERE child_id=? AND claude_session_id!=''",
            (child_id,),
        )
        return result.rowcount


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

def add_card(session_id: str, child_id: str, card_id: str, card_type: str, card_json: str, url: str = "") -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO cards (session_id, child_id, card_id, card_type, card_json, url) VALUES (?,?,?,?,?,?)",
            (session_id, child_id, card_id, card_type, card_json, url),
        )


def list_cards(session_id: str) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT card_id, card_type, card_json, url, created_at FROM cards WHERE session_id=? ORDER BY created_at ASC",
            (session_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_latest_card(session_id: str):
    with _connect() as conn:
        row = conn.execute(
            "SELECT card_id, card_type, card_json, url FROM cards WHERE session_id=? ORDER BY created_at DESC LIMIT 1",
            (session_id,),
        ).fetchone()
    return dict(row) if row else None


def list_all_cards_for_gallery() -> list[dict]:
    """갤러리 슬라이드쇼용: 전체 카드 조회."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT c.card_id, c.card_type, c.card_json, c.url, c.created_at, s.name AS child_name "
            "FROM cards c JOIN sessions s ON c.session_id = s.session_id "
            "ORDER BY c.created_at ASC"
        ).fetchall()
    return [dict(r) for r in rows]


def delete_card(session_id: str, card_id: str) -> None:
    with _connect() as conn:
        conn.execute(
            "DELETE FROM cards WHERE session_id=? AND card_id=?",
            (session_id, card_id),
        )
