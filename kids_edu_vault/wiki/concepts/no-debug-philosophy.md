---
type: concept
status: active
tags:
  - concept
  - pedagogy
  - pilot
  - sans-kids
created: 2026-04-12
updated: 2026-04-12
---

# No-Debug Philosophy (아이와 디버깅하지 않기)

## 정의
- "아이들은 **절대** 디버깅할 필요가 없어야 한다"는 원칙. [[sans-kids-school-2025]]의 핵심 철학.
- 에러·예외 상황은 진행자가 30초 내에 백업으로 전환하거나, 코드 자체가 방어적이어서 크래시를 보여주지 않아야 한다.

## 왜 중요한가
- 아이의 집중·감정 에너지는 **완성 경험**에 쓰여야지, 문법 디버깅에 쓰이면 금방 이탈한다.
- 소아암 병동 파일럿 맥락에서는 피로도·집중 지속 시간이 더 짧다 ([[environ-kukrip-amsenter]]). "에러 만나면 탈락"은 파일럿 성공 지표([[okr-q2-jy]] KR1: 5명 이상 실습 완료)와 직결된다.
- [[fast-implementation-mode]] 결정의 근거 중 하나.

## 구성 요소 / 하위 원칙
- **Error-proof architecture**: 모든 game loop에 try-catch, 모든 객체에 기본값(`hero = hero || {...}`) 지정.
- **console.log 금지, 시각 피드백 우선**: `document.getElementById('status').innerText` 같은 화면 메시지로 대체.
- **30-second rule**: 문제가 30초 안에 해결 안 되면 백업 템플릿·브라우저 직접 열기 등으로 전환 (`workshop-materials/emergency-troubleshooting.md`).
- **긍정 리프레이밍**: 에러 발생 시 "에러가 났어요" → "좋은 발견이야!", F12 개발자 도구는 **닫아버리고** 진행.
- **마지막 작동 상태로 되돌리기**: Ctrl+Z 또는 템플릿 재로드. 원인 분석은 아이 앞에서 하지 않는다.

## 예시
```javascript
function safeGameLoop() {
    try {
        updateGame();
        drawGame();
    } catch (e) {
        showMessage("🔄 다시 시도 중...");
    }
    requestAnimationFrame(safeGameLoop);
}
```

## 파일럿 적용 포인트
- [[cline]] + [[gemini-2-5-flash]] 프롬프트에 "에러 발생 시 아이에게 보이는 메시지는 격려형으로 리라이트" 규칙을 넣는다.
- 운영자 가이드([[pilot-operator-guide]])에 30-second rule과 백업 템플릿 진입 절차를 명시한다.
- 게임 스타터 템플릿([[pilot-game-starter-template]])에 try-catch 래퍼와 기본값 가드를 기본 탑재한다.

## 관련
- [[sans-kids-school-2025]] · [[fast-implementation-mode]] · [[ai-persona-workflows]] · [[single-html-runtime]]
- 원본: `.raw/sans-kids-2025/CLAUDE.md`, `.raw/sans-kids-2025/workshop-materials/emergency-troubleshooting.md`
