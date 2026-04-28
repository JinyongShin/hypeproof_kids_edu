"""Inline E2E curriculum test + edge cases."""
import asyncio, json, time, aiohttp

BASE = "http://localhost:8000"
CHILD_ID = "e2e_inline_test"

SCENARIOS = [
    {"block": 0, "prompt": "별빛 숲에서 사는 날개 달린 고양이 캐릭터 만들어줘", "expect_card_type": "character"},
    {"block": 1, "prompt": "왼쪽 화살표 누르면 왼쪽으로 날아가게 해줘, 속도는 빠르게", "expect_card_type": "character"},
    {"block": 2, "prompt": "거기다 친구 캐릭터도 화면 오른쪽에 추가해줘, 반짝이는 물고기", "expect_card_type": "character"},
    {"block": 3, "prompt": "별 대신 하트로 바꿔줘, 색은 분홍색으로", "expect_card_type": "title"},
    {"block": 4, "prompt": "배경에 밤하늘을 추가하고, 별들이 반짝이게 해줘", "expect_card_type": "title"},
    {"block": 5, "prompt": "내가 어떻게 말했는지 정리해줘", "expect_card_type": None},
]

EDGE_CASES = [
    {"name": "english_input", "prompt": "make a cat character"},
    {"name": "long_input", "prompt": "고양이" * 100},
    {"name": "no_character_start", "prompt": "게임 시작해줘"},
    {"name": "special_chars", "prompt": "!@#$%^&*()_+{}[]|\\:\";<>?,./~`"},
    {"name": "empty_input", "prompt": ""},
]

async def run_block(session, idx, scenario):
    prompt = scenario["prompt"]
    print(f"\n--- Block {scenario['block']}: {prompt[:40]}...")
    result = {"block": scenario["block"], "success": False, "has_card": False, "has_text": False, "error": "", "time_ms": 0, "card_type": None}

    if idx == 0:
        async with session.post(f"{BASE}/sessions/{CHILD_ID}") as r:
            data = await r.json()
            sid = data["session_id"]
    else:
        async with session.get(f"{BASE}/sessions/{CHILD_ID}") as r:
            sessions = await r.json()
            sid = sessions[-1]["session_id"]

    ws_url = f"ws://localhost:8000/ws/chat/{CHILD_ID}?session_id={sid}"
    t0 = time.time()
    try:
        async with session.ws_connect(ws_url) as ws:
            await ws.send_json({"prompt": prompt})
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    event = json.loads(msg.data)
                    if event.get("type") == "text":
                        result["has_text"] = True
                    elif event.get("type") == "card":
                        result["has_card"] = True
                        cd = json.loads(event.get("card_json", "{}"))
                        result["card_type"] = cd.get("card_type", "?")
                    elif event.get("type") == "done":
                        result["success"] = True
                        break
                    elif event.get("type") == "error":
                        result["error"] = event.get("chunk", "error")
                        break
                if time.time() - t0 > 120:
                    result["error"] = "timeout"; break
    except Exception as e:
        result["error"] = str(e)

    result["time_ms"] = int((time.time() - t0) * 1000)
    status = "PASS" if result["success"] and not result["error"] else "FAIL"
    print(f"  [{status}] text={result['has_text']} card={result['has_card']} type={result['card_type']} {result['time_ms']}ms")
    if result["error"]: print(f"  ERROR: {result['error']}")
    return result

async def run_edge(session, case):
    name = case["name"]
    print(f"\n--- Edge: {name}: {case['prompt'][:40]}...")
    ec_id = f"edge_{name}_test"
    try:
        async with session.post(f"{BASE}/sessions/{ec_id}") as r:
            data = await r.json()
            sid = data["session_id"]
    except: sid = "unknown"

    ws_url = f"ws://localhost:8000/ws/chat/{ec_id}?session_id={sid}"
    result = {"name": name, "success": False, "has_text": False, "has_card": False, "error": "", "time_ms": 0, "response_preview": ""}
    t0 = time.time()
    try:
        async with session.ws_connect(ws_url) as ws:
            await ws.send_json({"prompt": case["prompt"]})
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    event = json.loads(msg.data)
                    if event.get("type") == "text":
                        result["has_text"] = True
                        result["response_preview"] = event.get("chunk", "")[:100]
                    elif event.get("type") == "card":
                        result["has_card"] = True
                    elif event.get("type") == "done":
                        result["success"] = True; break
                    elif event.get("type") == "error":
                        result["error"] = event.get("chunk", "error"); break
                if time.time() - t0 > 60:
                    result["error"] = "timeout"; break
    except Exception as e:
        result["error"] = str(e)
    result["time_ms"] = int((time.time() - t0) * 1000)
    print(f"  [{'PASS' if result['success'] else 'FAIL'}] text={result['has_text']} card={result['has_card']} {result['time_ms']}ms")
    if result["error"]: print(f"  ERROR: {result['error']}")
    return result

async def main():
    async with aiohttp.ClientSession() as session:
        r = await session.get(f"{BASE}/health")
        if r.status != 200:
            print("Server down"); return

        print("=== E2E CURRICULUM 6-BLOCK TEST ===")
        e2e_results = []
        for i, s in enumerate(SCENARIOS):
            r = await run_block(session, i, s)
            e2e_results.append(r)

        print(f"\n=== SUMMARY ===")
        passed = sum(1 for r in e2e_results if r["success"] and not r["error"])
        for r in e2e_results:
            s = "PASS" if r["success"] and not r["error"] else "FAIL"
            print(f"  Block {r['block']}: {s} ({r['time_ms']}ms)")
        print(f"  Passed: {passed}/{len(e2e_results)}")

        print("\n=== EDGE CASE TESTS ===")
        edge_results = []
        for ec in EDGE_CASES:
            r = await run_edge(session, ec)
            edge_results.append(r)

        # Spam test
        print("\n--- Edge: spam (3 rapid sends) ---")
        spam_id = "edge_spam_test"
        async with session.post(f"{BASE}/sessions/{spam_id}") as r:
            data = await r.json()
            sid = data["session_id"]
        spam_result = {"name": "spam", "success": False, "error": ""}
        t0 = time.time()
        try:
            async with session.ws_connect(f"ws://localhost:8000/ws/chat/{spam_id}?session_id={sid}") as ws:
                for j in range(3):
                    await ws.send_json({"prompt": f"스팸 테스트 {j+1}"})
                done = 0
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        event = json.loads(msg.data)
                        if event.get("type") == "done": done += 1
                        if done >= 3 or time.time() - t0 > 90:
                            spam_result["success"] = done >= 1
                            break
        except Exception as e:
            spam_result["error"] = str(e)
        spam_result["time_ms"] = int((time.time() - t0) * 1000)
        print(f"  [{'PASS' if spam_result['success'] else 'FAIL'}] {spam_result['time_ms']}ms")
        edge_results.append(spam_result)

        # Save results as JSON for later
        all_results = {"e2e": e2e_results, "edge": edge_results}
        print("\n=== ALL RESULTS JSON ===")
        print(json.dumps(all_results, ensure_ascii=False, indent=2))

asyncio.run(main())
