"""
Kids Edu FastAPI Backend
WebSocket /ws/chat/{child_id}?session_id={session_id} — Claude 스트리밍 + 게임 HTML 추출
REST: 로그인, 세션 CRUD, 게임 파일 서빙
"""

import asyncio
import json
import logging
import os
import shutil
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

from claude_runner import StreamEvent, _DATA_DIR, _sessions, reset_session, stream_claude

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "root")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "0000")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

# sessions.json 과 분리된 세션 메타 저장 (session_id → 생성 시각 + 마지막 game_url)
_SESSION_META_FILE = _DATA_DIR / "session_meta.json"
_session_meta: dict[str, dict] = {}
_meta_lock = asyncio.Lock()

# 채팅 히스토리 저장 (data/messages/{child_id}/{session_id}.json)
_messages_lock = asyncio.Lock()
_MESSAGES_BASE = _DATA_DIR / "messages"


def _messages_path(child_id: str, session_id: str) -> Path | None:
    """경로 순회 공격 방어 후 메시지 파일 경로 반환. 유효하지 않으면 None."""
    base = _MESSAGES_BASE.resolve()
    path = (_MESSAGES_BASE / child_id / f"{session_id}.json").resolve()
    return path if path.is_relative_to(base) else None


async def _load_messages(child_id: str, session_id: str) -> list[dict]:
    path = _messages_path(child_id, session_id)
    if path is None or not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


async def _append_messages(child_id: str, session_id: str, new_msgs: list[dict]) -> None:
    path = _messages_path(child_id, session_id)
    if path is None:
        raise ValueError("잘못된 child_id 또는 session_id")
    async with _messages_lock:
        existing = await _load_messages(child_id, session_id)
        updated = existing + new_msgs
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(updated, ensure_ascii=False, indent=2))
        tmp.replace(path)


def _load_session_meta():
    global _session_meta
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    if _SESSION_META_FILE.exists():
        try:
            _session_meta = json.loads(_SESSION_META_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            logger.warning("session_meta.json 손상, 초기화")
            _session_meta = {}


async def _save_session_meta():
    """_meta_lock 보유 중에 호출하지 말 것. 파일 쓰기는 tmp→rename으로 원자적."""
    async with _meta_lock:
        snapshot = dict(_session_meta)
    tmp = _SESSION_META_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
    tmp.replace(_SESSION_META_FILE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _load_session_meta()
    logger.info("Kids Edu Backend 시작")
    yield
    logger.info("Kids Edu Backend 종료")


app = FastAPI(title="Kids Edu Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://hypeproof-ai.xyz"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.post("/auth/login")
async def login(body: dict):
    username = body.get("username", "")
    password = body.get("password", "")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"child_id": username}
    raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸어요")


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

@app.get("/sessions/{child_id}")
async def list_sessions(child_id: str):
    """child_id 의 세션 목록 반환."""
    results = []
    for session_id, meta in _session_meta.items():
        if meta.get("child_id") == child_id:
            results.append({
                "session_id": session_id,
                "created_at": meta.get("created_at", ""),
                "last_game_url": meta.get("last_game_url", ""),
            })
    # 생성 시각 오름차순
    results.sort(key=lambda x: x["created_at"])
    return results


@app.post("/sessions/{child_id}")
async def create_session(child_id: str):
    """새 세션 생성. session_id = {child_id}_{YYYYMMDD_HHmmss}"""
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"{child_id}_{ts}"
    async with _meta_lock:
        _session_meta[session_id] = {
            "child_id": child_id,
            "created_at": datetime.now().isoformat(),
            "last_game_url": "",
        }
    await _save_session_meta()
    logger.info("[%s] 세션 생성: %s", child_id, session_id)
    return {"session_id": session_id}


@app.delete("/sessions/{child_id}/{session_id}")
async def delete_session(child_id: str, session_id: str):
    """세션 삭제 — session_meta + sessions.json + games 폴더 모두 제거."""
    async with _meta_lock:
        meta = _session_meta.get(session_id)
        if meta is None or meta.get("child_id") != child_id:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없어요")

    # 경로 순회 공격 방어
    games_base = (_DATA_DIR / "games").resolve()
    game_dir = (_DATA_DIR / "games" / child_id / session_id).resolve()
    if not game_dir.is_relative_to(games_base):
        raise HTTPException(status_code=400, detail="잘못된 요청이에요")

    # claude 세션 삭제
    reset_session(child_id, session_id)

    # 메타 삭제
    async with _meta_lock:
        _session_meta.pop(session_id, None)
    await _save_session_meta()

    # games 폴더 삭제
    if game_dir.exists():
        shutil.rmtree(game_dir, ignore_errors=True)

    # 채팅 히스토리 파일 삭제
    msg_path = _messages_path(child_id, session_id)
    if msg_path is not None and msg_path.exists():
        msg_path.unlink(missing_ok=True)

    logger.info("[%s] 세션 삭제: %s", child_id, session_id)
    return {"deleted": True}


# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------

@app.get("/sessions/{child_id}/{session_id}/messages")
async def get_messages(child_id: str, session_id: str):
    """세션의 채팅 히스토리 반환. 없으면 빈 배열."""
    return await _load_messages(child_id, session_id)


# ---------------------------------------------------------------------------
# Game file serving
# ---------------------------------------------------------------------------

@app.get("/games/{child_id}/{session_id}/{game_id}")
async def serve_game(child_id: str, session_id: str, game_id: str):
    """저장된 게임 HTML 파일 서빙."""
    games_base = (_DATA_DIR / "games").resolve()
    game_path = (_DATA_DIR / "games" / child_id / session_id / f"{game_id}.html").resolve()
    if not game_path.is_relative_to(games_base):
        raise HTTPException(status_code=400, detail="잘못된 요청이에요")
    if not game_path.exists():
        raise HTTPException(status_code=404, detail="게임 파일을 찾을 수 없어요")
    return FileResponse(str(game_path), media_type="text/html")


# ---------------------------------------------------------------------------
# WebSocket chat
# ---------------------------------------------------------------------------

@app.websocket("/ws/chat/{child_id}")
async def chat_ws(websocket: WebSocket, child_id: str):
    """
    어린이별 독립 채팅 WebSocket.
    쿼리스트링 필수: ?session_id={session_id}
    session_id 없으면 400 거부.

    클라이언트 → 서버: {"prompt": "별을 모으는 게임 만들어줘"}
    서버 → 클라이언트:
        {"type": "text",  "chunk": "..."}
        {"type": "game",  "game_url": "http://..."}
        {"type": "done",  "hint": "💡 ...", "session_id": "...", "game_url": "http://..."}
        {"type": "error", "chunk": "오류 메시지"}
    """
    session_id = websocket.query_params.get("session_id", "").strip()
    await websocket.accept()
    if not session_id:
        await websocket.close(code=4400, reason="session_id 쿼리스트링이 필요해요")
        return
    logger.info("[%s::%s] WebSocket 연결", child_id, session_id)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "chunk": "잘못된 요청 형식"})
                continue

            prompt = data.get("prompt", "").strip()
            if not prompt:
                continue

            logger.info("[%s::%s] 프롬프트 수신: %s", child_id, session_id, prompt[:60])

            assistant_text = ""
            async for event in stream_claude(prompt, child_id, session_id):
                payload: dict = {"type": event.type}
                if event.type == "text":
                    assistant_text += event.chunk or ""
                    payload["chunk"] = event.chunk
                elif event.type == "game":
                    payload["game_url"] = event.game_url
                elif event.type == "done":
                    payload["hint"] = event.hint
                    payload["session_id"] = event.session_id
                    payload["game_url"] = event.game_url
                    # 마지막 game_url 세션 메타에 반영
                    if event.game_url and session_id in _session_meta:
                        async with _meta_lock:
                            if session_id in _session_meta:
                                _session_meta[session_id]["last_game_url"] = event.game_url
                        await _save_session_meta()
                    # 채팅 히스토리 저장
                    try:
                        await _append_messages(child_id, session_id, [
                            {"role": "user", "text": prompt},
                            {"role": "assistant", "text": assistant_text},
                        ])
                    except Exception:
                        logger.exception("[%s::%s] 메시지 저장 실패", child_id, session_id)
                elif event.type == "error":
                    payload["chunk"] = event.chunk

                await websocket.send_json(payload)

    except WebSocketDisconnect:
        logger.info("[%s::%s] WebSocket 연결 해제", child_id, session_id)
    except Exception as e:
        logger.exception("[%s::%s] WebSocket 오류", child_id, session_id)
        try:
            await websocket.send_json({"type": "error", "chunk": str(e)})
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.post("/admin/reset/{child_id}")
async def admin_reset(child_id: str):
    """운영자용 child_id 전체 세션 리셋."""
    ok = reset_session(child_id)
    return {"reset": ok, "child_id": child_id}
