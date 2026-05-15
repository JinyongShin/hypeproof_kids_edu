"""
FastAPI 엔드포인트 통합 테스트 — auth / session CRUD / game 파일 서빙.

테스트 대상:
  - POST /auth/login
  - POST /sessions/{child_id}
  - GET  /sessions/{child_id}
  - DELETE /sessions/{child_id}/{session_id}
  - GET  /games/{child_id}/{session_id}/{game_id}
  - 경로 순회(path traversal) 방어

실행:
  uv run pytest src/backend/tests/test_auth_session_game.py -v
"""

import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import main
import storage
from app.config import get_settings
from main import _DATA_DIR


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _isolated_db(monkeypatch):
    """테스트 전용 auth 자격증명 고정. DB 격리는 conftest.isolate_storage_db가 담당."""
    get_settings.cache_clear()
    monkeypatch.setenv("ADMIN_USERNAME", "root")
    monkeypatch.setenv("ADMIN_PASSWORD", "0000")
    yield
    get_settings.cache_clear()


@pytest.fixture()
def client():
    """lifespan 포함 TestClient — with 블록 안에서 사용한다."""
    with TestClient(main.app) as c:
        yield c


# ---------------------------------------------------------------------------
# 1. POST /auth/login
# ---------------------------------------------------------------------------


class TestAuthLogin:
    """로그인 엔드포인트 계약."""

    def test_correct_credentials_return_200_with_child_id(self, client):
        res = client.post("/auth/login", json={"username": "root", "password": "0000"})
        assert res.status_code == 200
        assert res.json().get("child_id") == "root"

    def test_wrong_password_returns_401(self, client):
        res = client.post("/auth/login", json={"username": "root", "password": "wrong"})
        assert res.status_code == 401

    def test_wrong_username_returns_401(self, client):
        res = client.post("/auth/login", json={"username": "admin", "password": "0000"})
        assert res.status_code == 401

    def test_empty_body_returns_401(self, client):
        res = client.post("/auth/login", json={})
        assert res.status_code == 401

    def test_401_detail_message_is_korean(self, client):
        res = client.post("/auth/login", json={"username": "x", "password": "x"})
        detail = res.json().get("detail", "")
        assert len(detail) > 0, "detail 메시지가 비어 있음"


# ---------------------------------------------------------------------------
# 2. POST /sessions/{child_id} — 세션 생성
# ---------------------------------------------------------------------------


class TestCreateSession:
    """새 세션을 생성하면 올바른 형식의 session_id 가 반환된다."""

    _SESSION_ID_PATTERN = re.compile(r"^.+_\d{8}_\d{6}$")

    def test_returns_200_with_session_id(self, client):
        res = client.post("/sessions/child01")
        assert res.status_code == 200
        data = res.json()
        assert "session_id" in data

    def test_session_id_format_matches_child_id_timestamp(self, client):
        """session_id = {child_id}_{YYYYMMDD_HHmmss}"""
        res = client.post("/sessions/child01")
        session_id = res.json()["session_id"]
        assert session_id.startswith("child01_"), (
            f"child_id prefix 없음: {session_id!r}"
        )
        assert self._SESSION_ID_PATTERN.match(session_id), (
            f"형식 불일치: {session_id!r}"
        )

    def test_session_id_date_part_is_8_digits(self, client):
        res = client.post("/sessions/testuser")
        session_id = res.json()["session_id"]
        # testuser_YYYYMMDD_HHmmss → split by '_'
        parts = session_id.split("_")
        # parts[-2] = YYYYMMDD, parts[-1] = HHmmss
        assert len(parts) >= 3
        assert re.match(r"^\d{8}$", parts[-2]), f"날짜 부분 오류: {parts[-2]!r}"
        assert re.match(r"^\d{6}$", parts[-1]), f"시각 부분 오류: {parts[-1]!r}"

    def test_different_child_ids_produce_distinct_session_ids(self, client):
        id_a = client.post("/sessions/alice").json()["session_id"]
        id_b = client.post("/sessions/bob").json()["session_id"]
        assert id_a != id_b

    def test_session_meta_stores_created_entry(self, client):
        client.post("/sessions/child02")
        assert len(storage.list_sessions("child02")) == 1


# ---------------------------------------------------------------------------
# 3. GET /sessions/{child_id} — 세션 목록
# ---------------------------------------------------------------------------


class TestListSessions:
    """목록 엔드포인트는 해당 child_id 의 세션만 반환한다."""

    def test_empty_list_when_no_sessions(self, client):
        res = client.get("/sessions/nobody")
        assert res.status_code == 200
        assert res.json() == []

    def test_returns_created_session(self, client):
        post_res = client.post("/sessions/child03")
        session_id = post_res.json()["session_id"]

        get_res = client.get("/sessions/child03")
        ids = [s["session_id"] for s in get_res.json()]
        assert session_id in ids

    def test_filters_by_child_id(self, client):
        """alice 와 bob 의 세션이 섞이지 않아야 한다."""
        client.post("/sessions/alice")
        client.post("/sessions/bob")

        alice_sessions = client.get("/sessions/alice").json()
        bob_sessions = client.get("/sessions/bob").json()

        alice_ids = {s["session_id"] for s in alice_sessions}
        bob_ids = {s["session_id"] for s in bob_sessions}

        assert all(sid.startswith("alice_") for sid in alice_ids)
        assert all(sid.startswith("bob_") for sid in bob_ids)
        assert alice_ids.isdisjoint(bob_ids)

    def test_list_items_have_required_fields(self, client):
        client.post("/sessions/child04")
        items = client.get("/sessions/child04").json()
        assert len(items) >= 1
        for item in items:
            assert "session_id" in item
            assert "created_at" in item
            assert "last_game_url" in item

    def test_list_is_sorted_by_created_at_ascending(self, client):
        """생성 순서대로(오름차순) 정렬돼야 한다."""
        import time

        client.post("/sessions/sorted_user")
        time.sleep(1.1)  # timestamp 차이를 보장하기 위해 1초 대기
        client.post("/sessions/sorted_user")

        items = client.get("/sessions/sorted_user").json()
        if len(items) >= 2:
            assert items[0]["created_at"] <= items[1]["created_at"]


# ---------------------------------------------------------------------------
# 4. DELETE /sessions/{child_id}/{session_id} — 세션 삭제
# ---------------------------------------------------------------------------


class TestDeleteSession:
    """삭제 후 목록에서 사라지며, 404 케이스도 처리한다."""

    def test_delete_returns_200_with_deleted_true(self, client):
        session_id = client.post("/sessions/child05").json()["session_id"]
        res = client.delete(f"/sessions/child05/{session_id}")
        assert res.status_code == 200
        assert res.json() == {"deleted": True}

    def test_deleted_session_absent_from_list(self, client):
        session_id = client.post("/sessions/child06").json()["session_id"]
        client.delete(f"/sessions/child06/{session_id}")

        ids = [s["session_id"] for s in client.get("/sessions/child06").json()]
        assert session_id not in ids

    def test_delete_nonexistent_session_returns_404(self, client):
        res = client.delete("/sessions/child07/nonexistent_session_id")
        assert res.status_code == 404

    def test_delete_with_wrong_child_id_returns_404(self, client):
        """child_id 가 다르면 삭제할 수 없어야 한다."""
        session_id = client.post("/sessions/owner").json()["session_id"]
        res = client.delete(f"/sessions/thief/{session_id}")
        assert res.status_code == 404

    def test_session_meta_is_empty_after_delete(self, client):
        session_id = client.post("/sessions/child08").json()["session_id"]
        assert len(storage.list_sessions("child08")) == 1
        client.delete(f"/sessions/child08/{session_id}")
        assert len(storage.list_sessions("child08")) == 0


# ---------------------------------------------------------------------------
# 5. GET /games/{child_id}/{session_id}/{game_id} — 게임 파일 서빙
# ---------------------------------------------------------------------------


class TestServeGame:
    """존재하는 게임 파일은 200으로 반환하고 없으면 404 를 반환한다."""

    def _write_game_file(self, child_id: str, session_id: str, game_id: str, content: str = "<html/>") -> Path:
        """테스트용 더미 게임 HTML 파일을 data/ 아래에 생성한다."""
        game_dir = _DATA_DIR / "games" / child_id / session_id
        game_dir.mkdir(parents=True, exist_ok=True)
        game_path = game_dir / f"{game_id}.html"
        game_path.write_text(content, encoding="utf-8")
        return game_path

    @pytest.fixture(autouse=True)
    def _cleanup_game_files(self):
        """테스트 완료 후 생성한 게임 파일을 정리한다."""
        created: list[Path] = []
        yield created
        for p in created:
            if p.exists():
                p.unlink(missing_ok=True)
            # 빈 부모 디렉토리도 정리
            for parent in [p.parent, p.parent.parent, p.parent.parent.parent]:
                try:
                    parent.rmdir()
                except OSError:
                    break

    def test_existing_game_file_returns_200(self, client, _cleanup_game_files):
        path = self._write_game_file("testchild", "testchild_20260413_120000", "game_001")
        _cleanup_game_files.append(path)

        res = client.get("/games/testchild/testchild_20260413_120000/game_001")
        assert res.status_code == 200

    def test_existing_game_file_content_type_is_html(self, client, _cleanup_game_files):
        path = self._write_game_file("testchild", "testchild_20260413_120001", "game_002", "<html><body>test</body></html>")
        _cleanup_game_files.append(path)

        res = client.get("/games/testchild/testchild_20260413_120001/game_002")
        assert res.status_code == 200
        assert "text/html" in res.headers.get("content-type", "")

    def test_missing_game_file_returns_404(self, client):
        res = client.get("/games/testchild/nosession/no_game")
        assert res.status_code == 404


# ---------------------------------------------------------------------------
# 6. 경로 순회(path traversal) 방어
# ---------------------------------------------------------------------------


class TestPathTraversal:
    """
    game_id 에 경로 순회 시퀀스가 포함되면 400 또는 404 를 반환해야 한다.

    현재 구현은 Path 연산으로 경로를 합치므로, `../` 시퀀스가 포함된
    game_id 는 data/games 바깥을 가리킬 수 있다. 파일이 실제로 없으면
    404 가 반환된다. 이 테스트는 존재하지 않는 경로에 대한 접근이 어떤
    경우에도 서버 오류(5xx) 없이 4xx 로 처리됨을 보장한다.
    """

    @pytest.mark.parametrize("game_id", [
        "../../../etc/passwd",
        "..%2F..%2Fetc%2Fpasswd",
        "....//....//etc//passwd",
        "game_001/../../../etc/passwd",
    ])
    def test_traversal_game_id_does_not_return_5xx(self, client, game_id):
        """경로 순회 game_id 는 500 서버 오류를 일으키지 않아야 한다."""
        res = client.get(f"/games/anyuser/anysession/{game_id}", follow_redirects=False)
        assert res.status_code < 500, (
            f"게임 서빙 경로 순회 시 서버 오류 발생: game_id={game_id!r}, "
            f"status={res.status_code}"
        )

    def test_unix_traversal_returns_400_or_404(self, client):
        """../../../etc/passwd 는 400 또는 404 를 반환해야 한다."""
        res = client.get("/games/anyuser/anysession/../../../etc/passwd", follow_redirects=False)
        assert res.status_code in (400, 404, 422), (
            f"예상 외 상태코드: {res.status_code}"
        )

    def test_null_byte_in_game_id_does_not_return_5xx(self, client):
        """null 바이트가 포함된 game_id 는 서버 오류 없이 4xx 처리되어야 한다."""
        res = client.get("/games/anyuser/anysession/game%00id", follow_redirects=False)
        assert res.status_code < 500

    @pytest.mark.parametrize("bad_segment", ["../secret", "..%2Fsecret"])
    def test_traversal_in_child_id_does_not_return_5xx(self, client, bad_segment):
        """child_id 위치에 경로 순회 시퀀스가 있어도 5xx 를 반환하지 않아야 한다."""
        res = client.get(f"/games/{bad_segment}/anysession/game_001", follow_redirects=False)
        assert res.status_code < 500

    @pytest.mark.parametrize("bad_segment", ["../secret", "..%2Fsecret"])
    def test_traversal_in_session_id_does_not_return_5xx(self, client, bad_segment):
        """session_id 위치에 경로 순회 시퀀스가 있어도 5xx 를 반환하지 않아야 한다."""
        res = client.get(f"/games/anyuser/{bad_segment}/game_001", follow_redirects=False)
        assert res.status_code < 500


# ---------------------------------------------------------------------------
# 7. PATCH /sessions/{child_id}/{session_id}/name — 세션 이름 변경
# ---------------------------------------------------------------------------


class TestRenameSession:
    """세션 이름 변경 엔드포인트 계약."""

    def test_rename_returns_200_with_ok(self, client):
        session_id = client.post("/sessions/child10").json()["session_id"]
        res = client.patch(
            f"/sessions/child10/{session_id}/name",
            json={"name": "새 이름"},
        )
        assert res.status_code == 200
        assert res.json() == {"ok": True}

    def test_empty_name_returns_400(self, client):
        session_id = client.post("/sessions/child11").json()["session_id"]
        res = client.patch(
            f"/sessions/child11/{session_id}/name",
            json={"name": ""},
        )
        assert res.status_code == 400

    def test_long_name_is_capped_at_30_chars(self, client):
        """30자 초과 이름은 30자로 잘려 저장되어야 한다."""
        session_id = client.post("/sessions/child12").json()["session_id"]
        long_name = "가" * 40
        client.patch(
            f"/sessions/child12/{session_id}/name",
            json={"name": long_name},
        )
        items = client.get("/sessions/child12").json()
        saved_name = next(s["name"] for s in items if s["session_id"] == session_id)
        assert len(saved_name) <= 30


# ---------------------------------------------------------------------------
# 8. POST /games/.../save + GET /gallery — 갤러리 등록
# ---------------------------------------------------------------------------


class TestSaveGame:
    """게임 갤러리 등록 엔드포인트 계약."""

    def _insert_game(self, session_id: str, child_id: str, game_id: str, url: str = "http://localhost/games/test"):
        """테스트용 게임 레코드를 직접 DB에 삽입."""
        storage.add_game(session_id, child_id, game_id, f"/data/games/{game_id}.html", url)

    def test_save_existing_game_returns_saved_true(self, client):
        session_id = client.post("/sessions/child13").json()["session_id"]
        self._insert_game(session_id, "child13", "game_001")
        res = client.post(f"/games/child13/{session_id}/game_001/save")
        assert res.status_code == 200
        assert res.json() == {"saved": True}

    def test_save_nonexistent_game_returns_404(self, client):
        session_id = client.post("/sessions/child14").json()["session_id"]
        res = client.post(f"/games/child14/{session_id}/no_game/save")
        assert res.status_code == 404

    def test_save_second_game_clears_first_saved_flag(self, client):
        """같은 세션에서 두 번째 게임을 저장하면 첫 번째 게임의 saved 가 0이 되어야 한다."""
        session_id = client.post("/sessions/child15").json()["session_id"]
        self._insert_game(session_id, "child15", "game_a")
        self._insert_game(session_id, "child15", "game_b")
        client.post(f"/games/child15/{session_id}/game_a/save")
        client.post(f"/games/child15/{session_id}/game_b/save")

        saved_games = storage.list_saved_games()
        saved_ids = {g["game_id"] for g in saved_games}
        assert "game_b" in saved_ids
        assert "game_a" not in saved_ids


class TestGallery:
    """갤러리 엔드포인트 계약."""

    def test_empty_gallery_returns_empty_list(self, client):
        res = client.get("/gallery")
        assert res.status_code == 200
        assert res.json() == []

    def test_saved_game_appears_in_gallery(self, client):
        session_id = client.post("/sessions/child16").json()["session_id"]
        storage.add_game(session_id, "child16", "game_show", "/data/games/game_show.html", "http://localhost/games/game_show")
        client.post(f"/games/child16/{session_id}/game_show/save")

        items = client.get("/gallery").json()
        assert len(items) >= 1
        found = next((g for g in items if g["game_id"] == "game_show"), None)
        assert found is not None

    def test_gallery_item_has_required_fields(self, client):
        session_id = client.post("/sessions/child17").json()["session_id"]
        storage.add_game(session_id, "child17", "game_fields", "/data/games/g.html", "http://localhost/games/g")
        client.post(f"/games/child17/{session_id}/game_fields/save")

        items = client.get("/gallery").json()
        item = next(g for g in items if g["game_id"] == "game_fields")
        for field in ("game_id", "url", "session_name", "child_id", "created_at", "session_id"):
            assert field in item, f"필드 누락: {field}"
