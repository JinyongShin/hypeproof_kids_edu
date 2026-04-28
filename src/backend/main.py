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

            # 게임 요청 감지 → AI가 템플릿 파라미터 결정 → 빌드
            # 1차: 명시적 게임 생성 의도
            game_keywords = ['게임 만들', '게임 시작', '플레이', '놀자', '게임해', '시작해줘']
            is_game_request = any(kw in original_prompt for kw in game_keywords)
            # 2차: 이미 게임이 있는 세션에서 메카닉 변경 의도 (새 게임 빌드)
            mechanic_keywords = ['점프', '횡이동', '횡스크롤', '달리기', '장애물',
                                 '피하', '친구 찾', '같이 놀', '바꿔줘', '다른 게임']
            if not is_game_request:
                has_existing_game = bool(await asyncio.to_thread(storage.list_games, session_id))
                if has_existing_game and any(kw in original_prompt for kw in mechanic_keywords):
                    is_game_request = True
            if is_game_request:
                # === Spec composition 방식 ===
                # LLM에게 spec JSON을 emit하게 함. 4 메카닉 enumeration 대신
                # 부품(player movement, spawns[], world, goal)을 자유롭게 조합.
                cards = await asyncio.to_thread(storage.list_cards, session_id)
                latest_char = await asyncio.to_thread(
                    storage.get_latest_card_by_type, session_id, "character"
                )
                latest_world = await asyncio.to_thread(
                    storage.get_latest_card_by_type, session_id, "world"
                )
                char_card_obj = {}
                world_card_obj = {}
                if latest_char:
                    try:
                        char_card_obj = json.loads(latest_char["card_json"])
                    except Exception:
                        pass
                if latest_world:
                    try:
                        world_card_obj = json.loads(latest_world["card_json"])
                    except Exception:
                        pass
                card_summary = ""
                if char_card_obj:
                    card_summary += f"\n캐릭터: {char_card_obj.get('name', '?')} — {char_card_obj.get('description', '')}"
                if world_card_obj:
                    card_summary += f"\n세계: {world_card_obj.get('name', '?')} — {world_card_obj.get('description', '')}"

                # spec emitter prompt — 부품 라이브러리를 LLM에 전달
                spec_prompt = (
                    f'아이가 이렇게 말했어: "{original_prompt}"\n'
                    f'{card_summary}\n\n'
                    f'다음 JSON spec만 출력해 (다른 텍스트·마크다운 금지). 부품 조합으로 게임을 정의:\n\n'
                    f'## player.movement (캐릭터 이동 방식)\n'
                    f'- "free": WASD/화살표 4방향 자유 이동 (기본)\n'
                    f'- "x_fixed": x 고정, y만 이동 (수직 점프 게임)\n'
                    f'- "jump": 좌우 + 점프(스페이스). 중력 적용. 횡스크롤 점프 게임 ("점프/횡이동" 단어)\n'
                    f'- "swim": 4방향 + 중력 0 (떠다님)\n\n'
                    f'## spawns[] (등장 객체. 0~6개 자유)\n'
                    f'각 spawn = {{role, sprite, from, motion, rate, speed, score_delta, respawn_on_collect}}\n'
                    f'- role: "item"(모음+1), "hazard"(피함-1), "friend"(만남+1, respawn 추천)\n'
                    f'- sprite: 이모지 1개 (없으면 자동)\n'
                    f'- from: "top"(위에서) "bottom"(아래에서) "left"(좌측에서) "right"(우측에서) '
                    f'"alternating_lr"(좌우 번갈아) "static_grid_bottom"(바닥에 줄지어) "wandering"(임의)\n'
                    f'- motion: "fall" "rise" "horizontal" "sine" "static" "wandering"\n'
                    f'- rate: 0.005~0.08 (분당 spawn 빈도). static_*은 무시.\n'
                    f'- speed: 0.5~5\n\n'
                    f'## world\n'
                    f'- scroll: "none" | "horizontal" | "parallax" (점프 게임은 horizontal 추천)\n\n'
                    f'## goal\n'
                    f'- time_limit: 20~90 (초). 기본 45.\n'
                    f'- target_score: 0~30. 0=무제한, N=N점이면 조기 성공.\n\n'
                    f'## 예시 매핑\n'
                    f'- "별 모으기 게임" → free + spawns[item from=top motion=fall sprite=⭐]\n'
                    f'- "위험 피하면서 보석" → free + spawns[item from=top, hazard from=top]\n'
                    f'- "친구 5명 찾기" → free + spawns[friend wandering, respawn] + goal.target_score=5\n'
                    f'- "장애물 점프 게임" → jump + spawns[hazard from=right horizontal] + scroll=horizontal\n'
                    f'- "좌우에서 줄넘기 피하면서 바닥 목화" → jump + spawns[hazard alternating_lr horizontal, item static_grid_bottom static]\n\n'
                    f'아이의 의도를 부품 조합으로 옮겨. JSON만 출력:\n'
                    f'{{"player":{{"movement":"..."}},"spawns":[...],"world":{{"scroll":"none"}},"goal":{{"time_limit":45,"target_score":0}}}}'
                )
                # generate_spec() — TUTOR.md 카드 페르소나 안 쓰고 spec 전용 system prompt만 사용
                spec_raw = {}
                try:
                    spec_text = await generate_spec(spec_prompt)
                    if spec_text:
                        # 가장 큰 JSON 객체 매치 (LLM이 마크다운/설명을 섞어 보내도 추출)
                        jm = _re.search(r'\{[\s\S]*\}', spec_text)
                        if jm:
                            try:
                                spec_raw = json.loads(jm.group())
                            except json.JSONDecodeError:
                                logger.warning("[%s::%s] spec JSON 파싱 실패, 폴백 사용",
                                               child_id, session_id)
                except Exception:
                    logger.exception("[%s::%s] spec emit 실패", child_id, session_id)

                # spec 빌드 (검증·default 채움은 game_engine 내부에서)
                from game_engine import build_game_with_spec
                game_html = await asyncio.to_thread(
                    build_game_with_spec, spec_raw, char_card_obj, world_card_obj
                )

                import time as _time
                game_id = f"game_{int(_time.time() * 1000)}"
                game_dir = (_DATA_DIR / "games" / child_id / session_id).resolve()
                games_base = (_DATA_DIR / "games").resolve()
                game_url = ""
                if game_dir.is_relative_to(games_base):
                    game_dir.mkdir(parents=True, exist_ok=True)
                    game_file = game_dir / f"{game_id}.html"
                    game_file.write_text(game_html, encoding="utf-8")
                    game_url = f"{os.getenv('BACKEND_BASE_URL', 'http://localhost:8000')}/games/{child_id}/{session_id}/{game_id}"
                    try:
                        await asyncio.to_thread(
                            storage.add_game, session_id, child_id, game_id, str(game_file), game_url
                        )
                    except Exception:
                        logger.exception("[%s::%s] 게임 메타 DB 등록 실패", child_id, session_id)

                # 인트로 — spec에서 추출된 정보 기반
                from game_engine import validate_spec as _vs
                validated = _vs(spec_raw, char_svg=char_card_obj.get("image_svg", ""),
                                world_svg=world_card_obj.get("image_svg", ""),
                                char_name=char_card_obj.get("name", "모험가"))
                mv = validated["player"]["movement"]
                tlim = validated["goal"]["time_limit"]
                tgt = validated["goal"]["target_score"]
                control_hint = "스페이스/↑/탭 = 점프, ←→ = 좌우" if mv == "jump" else "방향키나 WASD로 움직여"
                goal_msg = f"{tlim}초 안에 " + (f"{tgt}점 모으면 끝!" if tgt > 0 else "최대한 많이!") if tlim > 0 else (f"{tgt}점 모으면 끝!" if tgt > 0 else "마음껏!")
                intro = f"와, 게임을 만들었어! 🎮\n\n{control_hint}\n\n{goal_msg}"

                await websocket.send_json({"type": "text", "chunk": intro})
                await websocket.send_json({"type": "game", "html": game_html, "game_url": game_url})
                await websocket.send_json({"type": "done", "hint": "게임을 해보고, 다음엔 '더 빠르게 해줘' 같이 바꿔봐!"})
                continue

            # 캐릭터·세계 카드 컨텍스트 동시 주입 — 세계 구축 단계에서 캐릭터 SVG를 보존·수정하도록.
            prompt = original_prompt
            latest_character = await asyncio.to_thread(
                storage.get_latest_card_by_type, session_id, "character"
            )
            latest_world = await asyncio.to_thread(
                storage.get_latest_card_by_type, session_id, "world"
            )
            context_lines = []
            if latest_character:
                context_lines.append(f"이전 캐릭터: {latest_character['card_json']}")
            if latest_world:
                context_lines.append(f"이전 세계: {latest_world['card_json']}")
            if context_lines:
                prompt = (
                    f"{original_prompt}\n\n---\n"
                    + "\n".join(context_lines)
                    + "\n수정 요청이면 위 카드를 기반으로 고쳐줘. 완전히 새 카드 요청이면 무시하고 새로 만들어."
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
                    elif event.type == "game":
                        payload["html"] = event.html
                        payload["game_url"] = event.game_url
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
