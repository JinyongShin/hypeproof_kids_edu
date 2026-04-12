"""
claude_runner.py 핵심 로직 TDD 테스트.

이 파일만 읽어도 각 함수가 어떤 계약(contract)을 갖는지 파악 가능해야 한다.

테스트 그룹:
  1. SessionStore  — child_id(str) ↔ claude_session_id(str) 영구 저장소
  2. _extract_hint — 응답 텍스트에서 💡 힌트 줄 추출
  3. _HTML_RE      — 응답 텍스트에서 ```html ... ``` 블록 추출
  4. reset_session — 운영자가 특정 아이의 세션을 초기화
  5. stream_claude — MOCK_CLAUDE=1 모드에서의 이벤트 시퀀스
"""

import json
import os
import re
from pathlib import Path

import pytest

# claude_runner 내부 심볼 직접 임포트 (public API + private util 모두 테스트)
from claude_runner import (
    SessionStore,
    StreamEvent,
    _HTML_RE,
    _extract_hint,
    reset_session,
    stream_claude,
)


# ---------------------------------------------------------------------------
# 1. SessionStore
# ---------------------------------------------------------------------------


class TestSessionStore:
    """SessionStore는 child_id → claude_session_id 매핑을 JSON 파일에 영구 저장한다."""

    def test_get_returns_none_for_unknown_child(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        assert store.get("unknown_child") is None

    def test_set_and_get_roundtrip(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        store["child_01"] = "session_abc"
        assert store.get("child_01") == "session_abc"

    def test_contains_returns_true_after_set(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        store["child_02"] = "session_xyz"
        assert "child_02" in store

    def test_contains_returns_false_for_unknown_child(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        assert "ghost" not in store

    def test_delete_removes_session(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        store["child_03"] = "session_del"
        del store["child_03"]
        assert store.get("child_03") is None
        assert "child_03" not in store

    def test_delete_nonexistent_does_not_raise(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        del store["nobody"]  # 존재하지 않아도 예외 없어야 함

    def test_persists_to_disk_after_set(self, tmp_path):
        path = tmp_path / "sessions.json"
        store = SessionStore(path)
        store["child_04"] = "session_persist"
        raw = json.loads(path.read_text())
        assert raw["child_04"] == "session_persist"

    def test_loads_existing_sessions_on_init(self, tmp_path):
        path = tmp_path / "sessions.json"
        path.write_text(json.dumps({"child_05": "session_preload"}))
        store = SessionStore(path)
        assert store.get("child_05") == "session_preload"

    def test_multiple_children_are_independent(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        store["child_a"] = "session_a"
        store["child_b"] = "session_b"
        assert store.get("child_a") == "session_a"
        assert store.get("child_b") == "session_b"

    def test_overwrite_updates_session(self, tmp_path):
        store = SessionStore(tmp_path / "sessions.json")
        store["child_06"] = "old_session"
        store["child_06"] = "new_session"
        assert store.get("child_06") == "new_session"


# ---------------------------------------------------------------------------
# 2. _extract_hint
# ---------------------------------------------------------------------------


class TestExtractHint:
    """_extract_hint는 응답 텍스트 마지막의 💡 로 시작하는 줄을 반환한다."""

    def test_returns_hint_line_starting_with_bulb(self):
        text = "게임을 만들었어!\n\n```html\n...\n```\n\n💡 다음엔 색깔도 지정해봐!"
        assert _extract_hint(text) == "💡 다음엔 색깔도 지정해봐!"

    def test_returns_empty_string_when_no_hint(self):
        text = "게임을 만들었어!\n\n```html\n...\n```"
        assert _extract_hint(text) == ""

    def test_returns_last_hint_when_multiple_exist(self):
        text = "💡 첫 번째 힌트\n중간 내용\n💡 마지막 힌트"
        assert _extract_hint(text) == "💡 마지막 힌트"

    def test_ignores_lines_not_starting_with_bulb(self):
        text = "이건 힌트 아님\n다음엔 더 잘해봐"
        assert _extract_hint(text) == ""

    def test_handles_whitespace_around_hint(self):
        text = "내용\n  💡 공백 앞에 있는 힌트  "
        assert _extract_hint(text) == "💡 공백 앞에 있는 힌트"


# ---------------------------------------------------------------------------
# 3. _HTML_RE (HTML 코드 블록 추출 정규식)
# ---------------------------------------------------------------------------


class TestHtmlRegex:
    """_HTML_RE는 응답에서 ```html ... ``` 블록의 내용을 추출한다."""

    def test_extracts_html_from_code_block(self):
        text = "게임 설명\n\n```html\n<html><body>hello</body></html>\n```\n\n💡 힌트"
        match = _HTML_RE.search(text)
        assert match is not None
        assert "<html>" in match.group(1)

    def test_returns_none_when_no_html_block(self):
        text = "HTML 블록 없는 응답입니다."
        assert _HTML_RE.search(text) is None

    def test_extracts_first_html_block_when_multiple(self):
        text = "```html\n<first/>\n```\n중간\n```html\n<second/>\n```"
        match = _HTML_RE.search(text)
        assert match is not None
        assert "<first/>" in match.group(1)
        assert "<second/>" not in match.group(1)

    def test_case_insensitive_html_fence(self):
        text = "```HTML\n<html></html>\n```"
        assert _HTML_RE.search(text) is not None

    def test_multiline_html_content_is_captured(self):
        html_content = "<html>\n<body>\n<p>멀티라인</p>\n</body>\n</html>"
        text = f"```html\n{html_content}\n```"
        match = _HTML_RE.search(text)
        assert match is not None
        assert "멀티라인" in match.group(1)


# ---------------------------------------------------------------------------
# 4. reset_session
# ---------------------------------------------------------------------------


class TestResetSession:
    """reset_session은 운영자가 특정 child의 Claude 세션을 초기화할 때 사용한다."""

    def test_reset_returns_true_and_removes_existing_session(self, tmp_path, monkeypatch):
        # _sessions 전역 객체를 임시 경로로 교체
        import claude_runner
        temp_store = SessionStore(tmp_path / "sessions.json")
        temp_store["child_07"] = "session_to_reset"
        monkeypatch.setattr(claude_runner, "_sessions", temp_store)

        result = reset_session("child_07")

        assert result is True
        assert temp_store.get("child_07") is None

    def test_reset_returns_false_for_unknown_child(self, tmp_path, monkeypatch):
        import claude_runner
        temp_store = SessionStore(tmp_path / "sessions.json")
        monkeypatch.setattr(claude_runner, "_sessions", temp_store)

        result = reset_session("nobody")

        assert result is False


# ---------------------------------------------------------------------------
# 5. stream_claude (MOCK_CLAUDE=1)
# ---------------------------------------------------------------------------


class TestStreamClaudeMock:
    """
    MOCK_CLAUDE=1 모드에서 stream_claude는 실제 Claude를 호출하지 않고
    하드코딩된 응답을 StreamEvent 시퀀스로 반환한다.

    이 테스트는 이벤트 타입 시퀀스와 계약을 검증한다:
      1. text 이벤트가 1개 이상 온다
      2. game 이벤트가 정확히 1개 오며 html 필드가 비어있지 않다
      3. done 이벤트가 마지막에 온다
      4. MOCK 모드에서는 세션이 저장되지 않는다
    """

    @pytest.fixture(autouse=True)
    def set_mock_env(self, monkeypatch, tmp_path):
        import claude_runner
        # MOCK_CLAUDE는 모듈 로드 시 평가되므로 변수를 직접 패치
        monkeypatch.setattr(claude_runner, "MOCK_CLAUDE", True)
        # 세션 저장소도 격리
        temp_store = SessionStore(tmp_path / "sessions.json")
        monkeypatch.setattr(claude_runner, "_sessions", temp_store)
        self.store = temp_store

    async def _collect(self, child_id: str, prompt: str) -> list[StreamEvent]:
        events = []
        async for event in stream_claude(prompt, child_id):
            events.append(event)
        return events

    async def test_mock_yields_at_least_one_text_event(self):
        events = await self._collect("child_mock", "별 모으는 게임 만들어줘")
        text_events = [e for e in events if e.type == "text"]
        assert len(text_events) >= 1

    async def test_mock_yields_exactly_one_game_event_with_html(self):
        events = await self._collect("child_mock", "게임 만들어줘")
        game_events = [e for e in events if e.type == "game"]
        assert len(game_events) == 1
        assert game_events[0].html.strip() != ""
        assert "<!DOCTYPE html>" in game_events[0].html or "<html" in game_events[0].html

    async def test_mock_done_event_is_last(self):
        events = await self._collect("child_mock", "게임 만들어줘")
        assert events[-1].type == "done"

    async def test_mock_done_event_has_hint(self):
        events = await self._collect("child_mock", "게임 만들어줘")
        done = events[-1]
        assert done.hint.startswith("💡")

    async def test_mock_no_error_events(self):
        events = await self._collect("child_mock", "게임 만들어줘")
        error_events = [e for e in events if e.type == "error"]
        assert len(error_events) == 0

    async def test_mock_does_not_persist_session(self):
        await self._collect("child_no_session", "게임 만들어줘")
        assert self.store.get("child_no_session") is None
