"""커리큘럼 6블록 엔드투엔드 테스트"""
import asyncio, json, time
import aiohttp

BASE = "http://localhost:8000"
CHILD_ID = "e2e_curriculum_test"

SCENARIOS = [
    {"block": 0, "prompt": "별빛 숲에서 사는 날개 달린 고양이 캐릭터 만들어줘", "expect_card_type": "character"},
    {"block": 1, "prompt": "왼쪽 화살표 누르면 왼쪽으로 날아가게 해줘, 속도는 빠르게", "expect_card_type": "character"},
    {"block": 2, "prompt": "거기다 친구 캐릭터도 화면 오른쪽에 추가해줘, 반짝이는 물고기", "expect_card_type": "character"},
    {"block": 3, "prompt": "별 대신 하트로 바꿔줘, 색은 분홍색으로", "expect_card_type": "title"},
    {"block": 4, "prompt": "배경에 밤하늘을 추가하고, 별들이 반짝이게 해줘", "expect_card_type": "title"},
    {"block": 5, "prompt": "내가 어떻게 말했는지 정리해줘", "expect_card_type": None},
]

async def run_block(session, idx, scenario):
    prompt = scenario["prompt"]
    print(f"\n{'='*60}")
    print(f"Block {scenario['block']}: {prompt[:50]}")

    if idx == 0:
        async with session.post(f"{BASE}/sessions/{CHILD_ID}") as r:
            data = await r.json()
            session_id = data["session_id"]
            print(f"  세션 생성: {session_id}")
    else:
        async with session.get(f"{BASE}/sessions/{CHILD_ID}") as r:
            sessions = await r.json()
            if sessions:
                session_id = sessions[-1]["session_id"]

    ws_url = f"ws://localhost:8000/ws/chat/{CHILD_ID}?session_id={session_id}"
    result = {"block": scenario["block"], "success": False, "has_card": False, "has_hint": False, "has_text": False, "error": "", "time_ms": 0}

    t0 = time.time()

    async with session.ws_connect(ws_url) as ws:
        await ws.send_json({"prompt": prompt})

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                event = json.loads(msg.data)
                if event.get("type") == "text":
                    result["has_text"] = True
                elif event.get("type") == "card":
                    result["has_card"] = True
                    card_data = json.loads(event.get("card_json", "{}"))
                    card_type = card_data.get("card_type", "unknown")
                    result["card_type"] = card_type
                    print(f"  카드 타입: {card_type}")
                    if scenario["expect_card_type"] and card_type != scenario["expect_card_type"]:
                        result["error"] = f"카드 타입 불일치: 기대 {scenario['expect_card_type']}, 실제 {card_type}"
                elif event.get("type") == "done":
                    result["has_hint"] = bool(event.get("hint"))
                    result["success"] = True
                    if result["has_hint"]:
                        print(f"  힌트: {event['hint'][:60]}")
                    break
                elif event.get("type") == "error":
                    result["error"] = event.get("chunk", "unknown error")
                    break
            elif msg.type in (aiohttp.WSMsgType.ERROR, aiohttp.WSMsgType.CLOSED):
                result["error"] = "ws closed/error"
                break
            if time.time() - t0 > 60:
                result["error"] = "timeout 60s"
                break

    result["time_ms"] = int((time.time() - t0) * 1000)
    status = "PASS" if result["success"] and not result["error"] else "FAIL"
    print(f"  [{status}] 텍스트:{result['has_text']} 카드:{result['has_card']} 힌트:{result['has_hint']} 시간:{result['time_ms']}ms")
    if result["error"]:
        print(f"  WARNING: {result['error']}")
    return result

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            r = await session.get(f"{BASE}/health")
            if r.status != 200:
                print("FAIL: 서버 안 뜸"); return
        except:
            print("FAIL: 서버 안 뜸"); return

        print("커리큘럼 6블록 엔드투엔드 테스트")
        results = []
        for i, s in enumerate(SCENARIOS):
            r = await run_block(session, i, s)
            results.append(r)

        print(f"\n{'='*60}")
        print("요약")
        passed = sum(1 for r in results if r["success"] and not r["error"])
        for r in results:
            status = "PASS" if r["success"] and not r["error"] else "FAIL"
            print(f"  Block {r['block']}: {status} ({r.get('time_ms',0)}ms)")
        print(f"\n  통과: {passed}/{len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
