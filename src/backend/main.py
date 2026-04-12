"""
Kids Edu FastAPI Backend
WebSocket /ws/chat/{child_id} — Claude 스트리밍 + 게임 HTML 추출
"""

import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from claude_runner import StreamEvent, reset_session, stream_claude

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/chat/{child_id}")
async def chat_ws(websocket: WebSocket, child_id: str):
    """
    어린이별 독립 채팅 WebSocket.

    클라이언트 → 서버: {"prompt": "별을 모으는 게임 만들어줘"}
    서버 → 클라이언트:
        {"type": "text",  "chunk": "..."}        — 스트리밍 텍스트
        {"type": "game",  "html": "<!DOCTYPE..."}  — 실행 가능한 게임 HTML
        {"type": "done",  "hint": "💡 ...", "session_id": "..."}
        {"type": "error", "chunk": "오류 메시지"}
    """
    await websocket.accept()
    logger.info("[%s] WebSocket 연결", child_id)

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

            logger.info("[%s] 프롬프트 수신: %s", child_id, prompt[:60])

            async for event in stream_claude(prompt, child_id):
                payload: dict = {"type": event.type}
                if event.type == "text":
                    payload["chunk"] = event.chunk
                elif event.type == "game":
                    payload["html"] = event.html
                elif event.type == "done":
                    payload["hint"] = event.hint
                    payload["session_id"] = event.session_id
                elif event.type == "error":
                    payload["chunk"] = event.chunk

                await websocket.send_json(payload)

    except WebSocketDisconnect:
        logger.info("[%s] WebSocket 연결 해제", child_id)
    except Exception as e:
        logger.exception("[%s] WebSocket 오류", child_id)
        try:
            await websocket.send_json({"type": "error", "chunk": str(e)})
        except Exception:
            pass


@app.post("/admin/reset/{child_id}")
async def admin_reset(child_id: str):
    """운영자용 세션 리셋."""
    ok = reset_session(child_id)
    return {"reset": ok, "child_id": child_id}
