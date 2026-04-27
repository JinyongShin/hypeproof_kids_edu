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
from genai_runner import generate_card, generate_image
from qr_generator import generate_qr_png

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "root")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "0000")

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
    await asyncio.to_thread(_migrate_json_to_sqlite)
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
    """갤러리 슬라이드쇼용: 전체 카드 조회."""
    cards = await asyncio.to_thread(storage.list_all_cards_for_gallery)
    result = []
    for c in cards:
        try:
            card_data = json.loads(c["card_json"])
            card_data["child_name"] = c["child_name"]
            card_data["card_id"] = c["card_id"]
            card_data["created_at"] = c["created_at"]
            result.append(card_data)
        except (json.JSONDecodeError, KeyError):
            continue
    return result


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

    assistant_text = ""
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

            # 이모지만 입력 또는 의미 없는 입력 차단 (한글/영문 최소 2자)
            import re as _re
            alpha_count = len(_re.sub(r'[^가-힣a-zA-Z0-9]', '', original_prompt))
            if alpha_count < 2:
                await websocket.send_json({"type": "error", "chunk": "조금 더 자세히 말해줄래? 어떤 캐릭터를 만들고 싶은지 알려줘!"})
                continue

            logger.info("[%s::%s] 프롬프트 수신: %s", child_id, session_id, original_prompt[:60])

            # Fix: user 메시지는 원본 프롬프트로 저장 (주입 전)
            await asyncio.to_thread(storage.append_message, session_id, child_id, "user", original_prompt)

            # 첫 메시지면 세션 이름 자동 갱신
            count = await asyncio.to_thread(storage.message_count, session_id)
            if count == 1:
                auto_name = original_prompt[:15].strip()
                await asyncio.to_thread(storage.update_session_name, session_id, auto_name)

            # 기존 게임이 있으면 파일 경로를 프롬프트에 주입 — Claude가 Read 도구로 읽어서 수정
            prompt = original_prompt
            # cards 기반으로 전환: 이전 카드 참고 필요하면 주입
            cards = await asyncio.to_thread(storage.list_cards, session_id)
            if cards:
                latest_card = cards[-1]
                prompt = (
                    f"{original_prompt}\n\n"
                    f"---\n"
                    f"이전 카드: {latest_card['card_json']}\n"
                    f"수정 요청이면 이 카드를 기반으로 고쳐줘. 완전히 새 카드 요청이면 무시하고 새로 만들어."
                )

            assistant_text = ""
            try:
                async for event in generate_card(prompt, child_id, session_id):
                    payload: dict = {"type": event.type}
                    if event.type == "text":
                        assistant_text += event.chunk or ""
                        payload["chunk"] = event.chunk
                    elif event.type == "card":
                        payload["card_json"] = event.card_json
                        payload["card_url"] = event.card_url
                    elif event.type == "done":
                        payload["hint"] = event.hint
                        payload["session_id"] = event.session_id
                        payload["game_url"] = event.game_url
                        # Fix 1: assistant 메시지 done 시점에 저장
                        try:
                            await asyncio.to_thread(
                                storage.append_message, session_id, child_id, "assistant", assistant_text
                            )
                        except Exception:
                            logger.exception("[%s::%s] assistant 메시지 저장 실패", child_id, session_id)
                        assistant_text = ""  # 저장 완료 후 초기화
                    elif event.type == "error":
                        payload["chunk"] = event.chunk

                    await websocket.send_json(payload)

            except Exception as inner_exc:
                logger.exception("[%s::%s] stream_claude 내부 오류: %s", child_id, session_id, inner_exc)
                await websocket.send_json({"type": "error", "chunk": "뭔가 잘못됐어. 다시 한 번 해볼까? 😅"})

    except WebSocketDisconnect:
        logger.info("[%s::%s] WebSocket 연결 해제", child_id, session_id)
        # Fix 1: 연결 해제 시 부분 응답 저장
        if assistant_text:
            try:
                await asyncio.to_thread(
                    storage.append_message, session_id, child_id, "assistant", assistant_text
                )
            except Exception:
                logger.exception("[%s::%s] 부분 응답 저장 실패", child_id, session_id)
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
