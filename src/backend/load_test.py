"""
40명 동시 접속 부하 테스트 스크립트.
Usage: python3 load_test.py [--count 40] [--url http://localhost:8000]
"""

import asyncio
import json
import time
import argparse
import aiohttp


async def simulate_child(session: aiohttp.ClientSession, idx: int, base_url: str) -> dict:
    child_id = f"test_child_{idx:03d}"
    result = {"child_id": child_id, "steps": [], "success": True, "error": ""}

    try:
        t0 = time.time()
        resp = await session.post(f"{base_url}/sessions/{child_id}")
        data = await resp.json()
        session_id = data["session_id"]
        result["steps"].append({"step": "create_session", "ms": int((time.time() - t0) * 1000)})

        t1 = time.time()
        ws_url = f"{base_url.replace('http', 'ws')}/ws/chat/{child_id}?session_id={session_id}"
        async with session.ws_connect(ws_url) as ws:
            await ws.send_json({"prompt": "토끼처럼 생긴 캐릭터 만들어줘"})
            chunks = 0
            card_received = False

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    event = json.loads(msg.data)
                    chunks += 1
                    if event.get("type") == "card":
                        card_received = True
                    if event.get("type") in ("done", "error"):
                        break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
                if time.time() - t1 > 60:
                    result["error"] = "timeout"
                    break

            elapsed = int((time.time() - t1) * 1000)
            result["steps"].append({"step": "chat_card", "ms": elapsed, "chunks": chunks, "card_received": card_received})
            if not card_received:
                result["success"] = False

    except Exception as e:
        result["success"] = False
        result["error"] = str(e)

    return result


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--url", type=str, default="http://localhost:8000")
    args = parser.parse_args()

    print(f"🚀 부하 테스트: {args.count}명 → {args.url}")
    async with aiohttp.ClientSession() as session:
        try:
            resp = await session.get(f"{args.url}/health")
            if resp.status != 200:
                print("❌ 서버 응답 없음"); return
        except Exception:
            print("❌ 서버 연결 실패"); return

        t_start = time.time()
        tasks = [simulate_child(session, i, args.url) for i in range(args.count)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed_total = int((time.time() - t_start) * 1000)

    success = sum(1 for r in results if isinstance(r, dict) and r["success"])
    fail = sum(1 for r in results if isinstance(r, dict) and not r["success"])
    chat_times = [s["ms"] for r in results if isinstance(r, dict) for s in r["steps"] if s["step"] == "chat_card"]

    print(f"\n📊 결과 ({elapsed_total/1000:.1f}초)")
    print(f"  성공 {success}/{args.count} | 실패 {fail}")
    if chat_times:
        print(f"  평균 {sum(chat_times)/len(chat_times):.0f}ms | 최소 {min(chat_times)}ms | 최대 {max(chat_times)}ms")


if __name__ == "__main__":
    asyncio.run(main())
