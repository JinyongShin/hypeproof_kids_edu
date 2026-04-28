import asyncio, json, time, aiohttp, sys
BASE = 'http://localhost:8000'

async def run(name, prompt):
    cid = f'edge_{name}'
    async with aiohttp.ClientSession() as s:
        try:
            async with s.post(f'{BASE}/sessions/{cid}') as r:
                sid = (await r.json())['session_id']
        except Exception as e:
            return {'name': name, 'success': False, 'error': f'session: {e}', 'time_ms': 0}
        ws_url = f'ws://localhost:8000/ws/chat/{cid}?session_id={sid}'
        t0 = time.time()
        r = {'name': name, 'success': False, 'has_text': False, 'has_card': False, 'error': '', 'time_ms': 0, 'preview': ''}
        try:
            async with s.ws_connect(ws_url) as ws:
                await ws.send_json({'prompt': prompt})
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        ev = json.loads(msg.data)
                        if ev.get('type') == 'text':
                            r['has_text'] = True
                            r['preview'] = ev.get('chunk','')[:80]
                        elif ev.get('type') == 'card':
                            r['has_card'] = True
                        elif ev.get('type') == 'done':
                            r['success'] = True; break
                        elif ev.get('type') == 'error':
                            r['error'] = ev.get('chunk','?'); break
                    if time.time()-t0 > 60:
                        r['error'] = 'timeout'; break
        except Exception as e:
            r['error'] = str(e)
        r['time_ms'] = int((time.time()-t0)*1000)
        return r

async def main():
    cases = [
        ('english', 'make a cat character'),
        ('long500', '고양이' * 100),
        ('no_char_start', '게임 시작해줘'),
        ('special', '!@#$%^&*()_+{}[]|:;<>?,./~'),
        ('empty', ''),
    ]
    results = []
    for name, prompt in cases:
        print(f'Running {name}...', flush=True)
        r = await run(name, prompt)
        s = 'PASS' if r['success'] and not r['error'] else 'FAIL'
        print(f'{name}: [{s}] text={r["has_text"]} card={r["has_card"]} {r["time_ms"]}ms', flush=True)
        if r['error']: print(f'  ERR: {r["error"]}', flush=True)
        if r['preview']: print(f'  PREVIEW: {r["preview"]}', flush=True)
        results.append(r)

    print('Running spam...', flush=True)
    cid = 'edge_spam3'
    async with aiohttp.ClientSession() as s:
        async with s.post(f'{BASE}/sessions/{cid}') as r: sid = (await r.json())['session_id']
        t0 = time.time()
        spam = {'name': 'spam', 'success': False, 'error': '', 'time_ms': 0, 'responses': 0}
        try:
            async with s.ws_connect(f'ws://localhost:8000/ws/chat/{cid}?session_id={sid}') as ws:
                for j in range(3): await ws.send_json({'prompt': f'스팸{j}'})
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        ev = json.loads(msg.data)
                        if ev.get('type') == 'done': spam['responses'] += 1
                        if spam['responses'] >= 3 or time.time()-t0 > 90: break
            spam['success'] = spam['responses'] >= 1
        except Exception as e: spam['error'] = str(e)
        spam['time_ms'] = int((time.time()-t0)*1000)
        s2 = 'PASS' if spam['success'] else 'FAIL'
        print(f'spam: [{s2}] responses={spam["responses"]} {spam["time_ms"]}ms', flush=True)
        if spam['error']: print(f'  ERR: {spam["error"]}', flush=True)
        results.append(spam)
    print('===JSON===', flush=True)
    print(json.dumps(results, ensure_ascii=False), flush=True)

asyncio.run(main())
