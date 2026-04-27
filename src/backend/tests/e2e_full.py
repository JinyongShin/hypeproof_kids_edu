import asyncio, aiohttp, json, time, sys

BASE = 'http://localhost:8000'

async def test_prompt(s, child_id, prompt, label, timeout=45):
    t0 = time.time()
    r = {'label': label, 'success': False, 'has_text': False, 'has_card': False, 'has_hint': False, 'card_type': '', 'error': '', 'time_ms': 0}
    try:
        async with s.post(f'{BASE}/sessions/{child_id}') as resp:
            data = await resp.json()
            sid = data['session_id']
        async with s.ws_connect(f'{BASE}/ws/chat/{child_id}?session_id={sid}') as ws:
            await ws.send_json({'prompt': prompt})
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    e = json.loads(msg.data)
                    if e.get('type') == 'text': r['has_text'] = True
                    elif e.get('type') == 'card':
                        r['has_card'] = True
                        cd = json.loads(e.get('card_json','{}'))
                        r['card_type'] = cd.get('card_type','')
                    elif e.get('type') == 'done':
                        r['has_hint'] = bool(e.get('hint'))
                        r['success'] = True
                        break
                    elif e.get('type') == 'error':
                        r['error'] = e.get('chunk','')[:80]
                        break
                if time.time() - t0 > timeout:
                    r['error'] = 'timeout'; break
    except Exception as ex:
        r['error'] = str(ex)[:80]
    r['time_ms'] = int((time.time()-t0)*1000)
    return r

async def main():
    async with aiohttp.ClientSession() as s:
        r = await s.get(f'{BASE}/health')
        if r.status != 200:
            print('FAIL: server down', flush=True); return
        
        print('=== CURRICULUM 6-BLOCK ===', flush=True)
        curriculum = [
            ('Block 0', '별빛 숲에서 사는 날개 달린 고양이 캐릭터 만들어줘'),
            ('Block 1', '왼쪽 화살표 누르면 왼쪽으로 날아가게 해줘, 속도는 빠르게'),
            ('Block 2', '거기다 친구 캐릭터도 화면 오른쪽에 추가해줘, 반짝이는 물고기'),
            ('Block 3', '별 대신 하트로 바꿔줘, 색은 분홍색으로'),
            ('Block 4', '배경에 밤하늘을 추가하고, 별들이 반짝이게 해줘'),
            ('Block 5', '내가 어떻게 말했는지 정리해줘'),
        ]
        for i, (label, prompt) in enumerate(curriculum):
            r = await test_prompt(s, f'cur_b{i}', prompt, label)
            st = 'PASS' if r['success'] and not r['error'] else 'FAIL'
            print(f'  {st} {r["label"]}: text={r["has_text"]} card={r["has_card"]}({r["card_type"]}) hint={r["has_hint"]} {r["time_ms"]}ms {r["error"]}', flush=True)
        
        print('', flush=True)
        print('=== EDGE CASES ===', flush=True)
        edges = [
            ('English', 'make a cat character'),
            ('Long 500+', '안녕하세요 저는 정말 멋진 캐릭터를 만들고 싶어요. ' * 30),
            ('Special chars', '!@#$%^&*()'),
            ('Empty', ''),
            ('No char start', '게임 시작해줘'),
        ]
        for i, (label, prompt) in enumerate(edges):
            r = await test_prompt(s, f'edge_{i}', prompt, label, timeout=20)
            st = 'PASS' if (r['success'] and not r['error']) or (r['error'] and label == 'Special chars') or (r['error'] and label == 'Empty') else 'FAIL'
            print(f'  {st} {r["label"]}: text={r["has_text"]} card={r["has_card"]} err={r["error"]} {r["time_ms"]}ms', flush=True)

asyncio.run(main())
