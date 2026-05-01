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
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

import storage
from claude_runner import StreamEvent, _DATA_DIR, reset_session, stream_claude
from genai_runner import generate_card, generate_image, generate_spec
from qr_generator import generate_qr_png


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# JSON → SQLite 마이그레이션 (서버 시작 시 1회)
# ---------------------------------------------------------------------------

_MIGRATION_DONE_FLAG = _DATA_DIR / "migration_done.flag"


def _migrate_json_to_sqlite() -> None:
    """session_meta.json + sessions.json + messages/ → SQLite. 완료 플래그 파일로 멱등성 보장."""
    if _MIGRATION_DONE_FLAG.exists():
        logger.info("SQLite 마이그레이션 이미 완료 (플래그 존재), 스킵")
        return

    migrated = 0

    # session_meta.json 읽기
    meta_file = _DATA_DIR / "session_meta.json"
    sessions_file = _DATA_DIR / "sessions.json"

    session_meta: dict = {}
    if meta_file.exists():
        try:
            session_meta = json.loads(meta_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, ValueError):
            logger.warning("session_meta.json 손상, 건너뜀")

    # sessions.json (claude_session_id 맵)
    claude_sessions: dict = {}
    if sessions_file.exists():
        try:
            raw = json.loads(sessions_file.read_text(encoding="utf-8"))
            # 복합키 포맷: "child_id::session_id" → claude_session_id
            claude_sessions = {k: v for k, v in raw.items() if "::" in k}
        except (json.JSONDecodeError, ValueError):
            logger.warning("sessions.json 손상, 건너뜀")

    for session_id, meta in session_meta.items():
        child_id = meta.get("child_id", "")
        if not child_id:
            continue
        created_at = meta.get("created_at", datetime.now().isoformat())
        name = meta.get("name", "")
        storage.create_session(session_id, child_id, name, created_at)

        # claude_session_id 복원
        key = f"{child_id}::{session_id}"
        if key in claude_sessions:
            storage.set_claude_session_id(session_id, claude_sessions[key])

        # 채팅 히스토리 복원
        msg_path = _DATA_DIR / "messages" / child_id / f"{session_id}.json"
        if msg_path.exists():
            try:
                msgs = json.loads(msg_path.read_text(encoding="utf-8"))
                for m in msgs:
                    role = m.get("role", "")
                    text = m.get("text", "")
                    if role and text:
                        storage.append_message(session_id, child_id, role, text)
            except (json.JSONDecodeError, ValueError):
                logger.warning("메시지 파일 손상 건너뜀: %s", msg_path)

        migrated += 1

    # 마이그레이션 완료 플래그 기록 (재시작 시 재실행 방지)
    _MIGRATION_DONE_FLAG.write_text("done", encoding="utf-8")
    logger.info("JSON→SQLite 마이그레이션 완료: %d세션", migrated)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_db()
    from app.auth import ensure_default_admin
    await ensure_default_admin()
    await asyncio.to_thread(_migrate_json_to_sqlite)
    from app.graph.graph import graph_lifespan
    async with graph_lifespan() as graph:
        app.state.graph = graph
        logger.info("Kids Edu Backend 시작")
        yield
    logger.info("Kids Edu Backend 종료")


app = FastAPI(title="Kids Edu Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    from app.auth import authenticate
    username = body.get("username", "")
    password = body.get("password", "")
    result = await authenticate(username, password)
    if result is None:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸어요")
    # child_id 키 유지 — 프론트엔드 호환
    return {"child_id": username, **result}


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------

@app.get("/sessions/{child_id}")
async def list_sessions(child_id: str):
    """child_id의 세션 목록 반환 (name, last_game_url 포함)."""
    return await asyncio.to_thread(storage.list_sessions, child_id)


@app.post("/sessions/{child_id}")
async def create_session(child_id: str):
    """새 세션 생성. name = '대화 N' 자동 할당."""
    sessions = await asyncio.to_thread(storage.list_sessions, child_id)
    name = f"대화 {len(sessions) + 1}"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = f"{child_id}_{ts}"
    created_at = datetime.now().isoformat()
    await asyncio.to_thread(storage.create_session, session_id, child_id, name, created_at)
    logger.info("[%s] 세션 생성: %s (%s)", child_id, session_id, name)
    return {"session_id": session_id, "name": name}


@app.delete("/sessions/{child_id}/{session_id}")
async def delete_session(child_id: str, session_id: str):
    """세션 삭제 — DB + games 폴더 모두 제거."""
    sessions = await asyncio.to_thread(storage.list_sessions, child_id)
    target = next((s for s in sessions if s["session_id"] == session_id), None)
    if target is None:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없어요")

    # 경로 순회 공격 방어
    games_base = (_DATA_DIR / "games").resolve()
    game_dir = (_DATA_DIR / "games" / child_id / session_id).resolve()
    if not game_dir.is_relative_to(games_base):
        raise HTTPException(status_code=400, detail="잘못된 요청이에요")

    # claude 세션 초기화
    reset_session(child_id, session_id)

    # DB 삭제 (messages + games + session)
    await asyncio.to_thread(storage.delete_session, session_id)

    # games 폴더 삭제
    if game_dir.exists():
        shutil.rmtree(game_dir, ignore_errors=True)

    logger.info("[%s] 세션 삭제: %s", child_id, session_id)
    return {"deleted": True}


@app.patch("/sessions/{child_id}/{session_id}/name")
async def rename_session(child_id: str, session_id: str, body: dict):
    """세션 이름 수동 변경."""
    name = body.get("name", "").strip()[:30]
    if not name:
        raise HTTPException(status_code=400, detail="이름을 입력해주세요")
    await asyncio.to_thread(storage.update_session_name, session_id, name)
    return {"ok": True}


# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------

@app.get("/sessions/{child_id}/{session_id}/messages")
async def get_messages(child_id: str, session_id: str):
    """세션의 채팅 히스토리 반환. 없으면 빈 배열."""
    return await asyncio.to_thread(storage.load_messages, session_id)


# ---------------------------------------------------------------------------
# QR code
# ---------------------------------------------------------------------------

@app.get("/qr/{child_id}/{session_id}/{card_id}")
async def get_qr(child_id: str, session_id: str, card_id: str):
    """카드 URL을 QR PNG로 반환."""
    card_url = f"{os.getenv('BACKEND_BASE_URL', 'http://localhost:8000')}/cards/{child_id}/{session_id}/{card_id}"
    png_bytes = await asyncio.to_thread(generate_qr_png, card_url, child_id)
    return Response(content=png_bytes, media_type="image/png")


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

@app.get("/cards/{child_id}/{session_id}/{card_id}")
async def get_card(child_id: str, session_id: str, card_id: str):
    """카드 JSON 데이터 반환."""
    card = await asyncio.to_thread(storage.get_latest_card, session_id)
    if card is None or card["card_id"] != card_id:
        cards = await asyncio.to_thread(storage.list_cards, session_id)
        card = next((c for c in cards if c["card_id"] == card_id), None)
    if card is None:
        raise HTTPException(status_code=404, detail="카드를 찾을 수 없어요")
    return json.loads(card["card_json"])


@app.get("/gallery")
async def gallery():
    """런칭쇼: 저장된(saved=1) 게임 목록. 각 항목 = {game_id, url, session_name, child_id, created_at, session_id}."""
    return await asyncio.to_thread(storage.list_saved_games)


@app.post("/generate-image")
async def generate_image_endpoint(body: dict):
    """프론트엔드에서 image_prompt로 이미지 생성 요청."""
    image_prompt = body.get("image_prompt", "").strip()
    if not image_prompt:
        raise HTTPException(status_code=400, detail="image_prompt가 필요해요")
    try:
        image_bytes, mime_type = await generate_image(image_prompt)
        import base64
        return {"image_base64": base64.b64encode(image_bytes).decode("utf-8"), "mime_type": mime_type}
    except Exception as e:
        logger.exception("이미지 생성 오류: %s", e)
        raise HTTPException(status_code=500, detail="이미지 생성에 실패했어요")


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


@app.post("/games/{child_id}/{session_id}/{game_id}/save")
async def save_game(child_id: str, session_id: str, game_id: str):
    """게임을 갤러리(런칭쇼)에 등록.
    동일 세션의 기존 저장 게임이 있으면 자동 덮어쓰기 (saved=0 → 새 게임 saved=1)."""
    ok = await asyncio.to_thread(storage.mark_game_saved, session_id, game_id)
    if not ok:
        raise HTTPException(status_code=404, detail="해당 게임을 찾을 수 없어요")
    logger.info("[%s::%s] 게임 저장(런칭쇼 등록): %s", child_id, session_id, game_id)
    return {"saved": True}


@app.get("/preview-game")
async def preview_game(
    type: str = "collect",
    char_name: str = "테스트 캐릭터",
    char_emoji: str = "🐰",
    item_emoji: str = "⭐",
    hazard_emoji: str = "💧",
    friend_emoji: str = "🐰",
    bg_theme: str = "우주",
    pace: float = 1.0,
    time: int = 45,
    target: int = 0,
):
    """개발자용 빠른 미리보기. 채팅·세션·LLM 흐름 우회. 쿼리스트링으로 파라미터 전달.
    예: /preview-game?type=dodge&char_emoji=🤖&item_emoji=⭐&hazard_emoji=💀
    SVG 입력은 파라미터 너무 길어 지원 X — 실제 흐름에서만 SVG 검증.
    """
    from game_template import build_game_with_params
    fake_cards = [
        json.dumps({
            "card_type": "character",
            "name": char_name,
            "image_svg": "",
        }),
        json.dumps({
            "card_type": "world",
            "name": f"테스트 {bg_theme}",
            "world": bg_theme,
            "description": f"{bg_theme} 배경의 세계",
            "image_svg": "",
        }),
    ]
    params = {
        "game_type": type,
        "char_emoji": char_emoji,
        "item_emoji": item_emoji,
        "hazard_emoji": hazard_emoji,
        "friend_emoji": friend_emoji,
        "bg_theme": bg_theme,
        "pace_scale": pace,
        "time_limit": time,
        "target_score": target,
    }
    html = await asyncio.to_thread(build_game_with_params, fake_cards, params, "")
    return Response(content=html, media_type="text/html")


@app.get("/preview-spec")
async def preview_spec(spec: str = "", preset: str = ""):
    """Spec composition 엔진 dev 미리보기.
    spec= 쿼리에 JSON 문자열, 또는 preset= 으로 사전 정의된 케이스 4종(collect/dodge/chase/jump).

    예시:
      /preview-spec?preset=jump
      /preview-spec?preset=monkey  (사용자 원숭이 케이스: 좌우 줄넘기 + 바닥 목화)
      /preview-spec?spec={"player":{"movement":"jump"},"spawns":[...]}
    """
    from game_engine import (
        build_game_with_spec, spec_for_collect, spec_for_dodge,
        spec_for_chase, spec_for_jump,
    )
    if preset:
        if preset == "collect":
            spec_obj = spec_for_collect("⭐")
        elif preset == "dodge":
            spec_obj = spec_for_dodge("⭐", "💀")
        elif preset == "chase":
            spec_obj = spec_for_chase("🐰")
        elif preset == "jump":
            spec_obj = spec_for_jump("⭐", "🌵")
        elif preset == "monkey":
            # 사용자 원숭이 케이스: 좌우 줄넘기 점프 피하기 + 바닥 목화 모으기
            spec_obj = {
                "player": {"movement": "jump"},
                "spawns": [
                    {"role": "hazard", "from": "alternating_lr",
                     "motion": "horizontal", "sprite": "🪢",
                     "rate": 0.025, "speed": 3},
                    {"role": "item", "from": "static_grid_bottom",
                     "motion": "static", "sprite": "☁️",
                     "score_delta": 1, "respawn_on_collect": False},
                ],
                "world": {"scroll": "none"},
                "goal": {"time_limit": 45, "target_score": 0},
            }
        else:
            raise HTTPException(status_code=400, detail="알 수 없는 preset")
    else:
        if not spec:
            raise HTTPException(status_code=400, detail="spec 또는 preset 필요")
        try:
            spec_obj = json.loads(spec)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="spec JSON 파싱 실패")
    html = await asyncio.to_thread(build_game_with_spec, spec_obj, None, None)
    return Response(content=html, media_type="text/html")


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
        {"type": "card",  "card_json": "...", "card_url": "..."}
        {"type": "game",  "html": "...", "game_url": "http://..."}
        {"type": "done",  "hint": "...", "session_id": "...", "game_url": "http://..."}
        {"type": "error", "chunk": "오류 메시지"}
    """
    from ws_handler import handle_chat_message
    import re as _re

    session_id = websocket.query_params.get("session_id", "").strip()
    await websocket.accept()
    if not session_id:
        await websocket.close(code=4400, reason="session_id 쿼리스트링이 필요해요")
        return
    logger.info("[%s::%s] WebSocket 연결", child_id, session_id)

    graph = app.state.graph

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "chunk": "잘못된 요청 형식"})
                continue

            original_prompt = data.get("prompt", "").strip()
            if not original_prompt:
                await websocket.send_json({"type": "error", "chunk": "뭐라고 말하고 싶은지 입력해줘!"})
                continue

            alpha_count = len(_re.sub(r'[^가-힣a-zA-Z0-9]', '', original_prompt))
            if alpha_count < 2:
                await websocket.send_json({"type": "error", "chunk": "조금 더 자세히 말해줄래? 어떤 캐릭터를 만들고 싶은지 알려줘!"})
                continue

            logger.info("[%s::%s] 프롬프트 수신: %s", child_id, session_id, original_prompt[:60])

            await asyncio.to_thread(storage.append_message, session_id, child_id, "user", original_prompt)

            count = await asyncio.to_thread(storage.message_count, session_id)
            if count == 1:
                auto_name = original_prompt[:15].strip()
                await asyncio.to_thread(storage.update_session_name, session_id, auto_name)

            await handle_chat_message(websocket, original_prompt, child_id, session_id, graph)

    except WebSocketDisconnect:
        logger.info("[%s::%s] WebSocket 연결 해제", child_id, session_id)
    except Exception as e:
        logger.exception("[%s::%s] WebSocket 오류: %s", child_id, session_id, e)
        try:
            await websocket.send_json({"type": "error", "chunk": "뭔가 잘못됐어. 다시 한 번 해볼까? 😅"})
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
