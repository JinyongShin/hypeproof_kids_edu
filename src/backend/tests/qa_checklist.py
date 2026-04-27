import asyncio, json, time
import aiohttp

BASE = 'http://localhost:8000'

BANNED_KEYWORDS = ['죽음', '죽이', '살해', '전투', '적 ', '무기', '칼', '총', '피투성이', '타격', '공격', '처형']
CHILD_TONE = ['해볼까', '야!', '만들어', '멋진', '귀엽', '신나', '대단']

async def test_and_qa(s, child_id, prompt, label, expected_card_type=None, timeout=45):
    t0 = time.time()
    r = {
        'label': label, 'success': False, 'checks': {},
        'has_text': False, 'has_card': False, 'has_hint': False,
        'card_type': '', 'card_name': '', 'card_desc': '',
        'hint_text': '', 'image_url': '', 'full_text': '',
        'error': '', 'time_ms': 0, 'qa_score': 0, 'banned_found': [],
    }
    try:
        async with s.post(BASE + '/sessions/' + child_id) as resp:
            data = await resp.json()
            sid = data['session_id']
        ws_url = BASE + '/ws/chat/' + child_id + '?session_id=' + sid
        async with s.ws_connect(ws_url) as ws:
            await ws.send_json({'prompt': prompt})
            chunks = []
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    e = json.loads(msg.data)
                    et = e.get('type', '')
                    if et == 'text' and e.get('chunk'):
                        chunks.append(e['chunk'])
                        r['has_text'] = True
                    elif et == 'card':
                        r['has_card'] = True
                        r['image_url'] = e.get('card_url', '')
                        try:
                            cd = json.loads(e.get('card_json', '{}'))
                            r['card_type'] = cd.get('card_type', '')
                            r['card_name'] = cd.get('name', '')
                            r['card_desc'] = cd.get('description', '')
                        except:
                            pass
                    elif et == 'done':
                        r['has_hint'] = bool(e.get('hint'))
                        r['hint_text'] = e.get('hint', '')
                        r['success'] = True
                        break
                    elif et == 'error':
                        r['error'] = e.get('chunk', '')[:100]
                        break
                if time.time() - t0 > timeout:
                    r['error'] = 'timeout'
                    break
    except Exception as ex:
        r['error'] = str(ex)[:100]

    r['time_ms'] = int((time.time() - t0) * 1000)
    r['full_text'] = ' '.join(chunks)

    c = {}
    c['01_json'] = r['has_card']
    c['02_type'] = (not expected_card_type) or (r['card_type'] == expected_card_type)
    c['03_name'] = len(r['card_name']) > 0
    c['04_desc'] = len(r['card_desc']) > 5
    banned = [kw for kw in BANNED_KEYWORDS if kw in r['full_text']]
    r['banned_found'] = banned
    c['05_coop'] = len(banned) == 0
    c['06_tone'] = any(t in r['full_text'] for t in CHILD_TONE)
    c['07_hint'] = r['has_hint'] and len(r['hint_text']) > 5
    c['08_nocode'] = '```' not in r['full_text'].replace('```json', '').replace('```', '')
    c['09_image'] = len(r['image_url']) > 0
    c['10_time'] = r['time_ms'] < 30000
    r['checks'] = c
    passed = sum(1 for v in c.values() if v)
    r['qa_score'] = passed / len(c) if c else 0
    return r


async def main():
    async with aiohttp.ClientSession() as s:
        try:
            resp = await s.get(BASE + '/health')
            if resp.status != 200:
                print('FAIL: server down', flush=True)
                return
        except:
            print('FAIL: server down', flush=True)
            return

        curriculum = [
            ('Block0_character', '별빛 숲에서 사는 날개 달린 고양이 캐릭터 만들어줘', 'character'),
            ('Block1_specify', '왼쪽 화살표 누르면 왼쪽으로 날아가게 해줘, 속도는 빠르게', None),
            ('Block2_add', '거기다 친구 캐릭터도 화면 오른쪽에 추가해줘, 반짝이는 물고기', None),
            ('Block3_modify', '별 대신 하트로 바꿔줘, 색은 분홍색으로', None),
            ('Block4_free', '배경에 밤하늘을 추가하고, 별들이 반짝이게 해줘', None),
            ('Block5_lang', '내가 어떻게 말했는지 정리해줘', None),
        ]
        edges = [
            ('Edge_en', 'make a cat character', None),
            ('Edge_long', '안녕하세요 저는 정말 멋진 캐릭터를 만들고 싶어요. ' * 30, None),
            ('Edge_special', '!@#$%^&*()', None),
            ('Edge_empty', '', None),
            ('Edge_nostart', '게임 시작해줘', None),
        ]

        all_results = []
        for i, (label, prompt, ect) in enumerate(curriculum):
            print('\n--- ' + label + ' ---', flush=True)
            r = await test_and_qa(s, 'qab' + str(i), prompt, label, ect)
            all_results.append(r)
            score = int(r['qa_score'] * 100)
            failed = [k for k, v in r['checks'].items() if not v]
            print('  Score:' + str(score) + '% Time:' + str(r['time_ms']) + 'ms Card:' + r['card_type'] + ' Name:' + r['card_name'], flush=True)
            if failed:
                print('  Failed: ' + ', '.join(failed), flush=True)
            if r['banned_found']:
                print('  BANNED: ' + str(r['banned_found']), flush=True)
            if r['error']:
                print('  Error: ' + r['error'], flush=True)

        print('\n--- EDGE CASES ---', flush=True)
        for i, (label, prompt, ect) in enumerate(edges):
            print('\n--- ' + label + ' ---', flush=True)
            r = await test_and_qa(s, 'qae' + str(i), prompt, label, ect, timeout=20)
            all_results.append(r)
            if r['error']:
                print('  Error: ' + r['error'], flush=True)
            else:
                score = int(r['qa_score'] * 100)
                print('  Score:' + str(score) + '% Time:' + str(r['time_ms']) + 'ms', flush=True)
            if r['banned_found']:
                print('  BANNED: ' + str(r['banned_found']), flush=True)

        print('\n\n=== SUMMARY ===', flush=True)
        passed = [r for r in all_results if r['success'] and not r['error']]
        failed_list = [r for r in all_results if not r['success'] or r['error']]
        avg_score = sum(r['qa_score'] for r in passed) / len(passed) if passed else 0
        print('Passed: ' + str(len(passed)) + '/' + str(len(all_results)), flush=True)
        print('Avg QA Score: ' + str(int(avg_score * 100)) + '%', flush=True)
        if failed_list:
            print('Failed:', flush=True)
            for r in failed_list:
                print('  - ' + r['label'] + ': ' + (r['error'] or 'qa checks failed'), flush=True)

if __name__ == '__main__':
    asyncio.run(main())
