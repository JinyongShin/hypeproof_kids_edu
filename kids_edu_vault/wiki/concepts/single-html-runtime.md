---
type: concept
status: active
tags:
  - concept
  - runtime
  - pilot
  - sans-kids
created: 2026-04-12
updated: 2026-04-12
---

# Single-HTML Runtime (단일 HTML 실행 모델)

## 정의
- HTML·CSS·JavaScript를 **하나의 .html 파일**에 인라인으로 담아, 빌드·서버·패키지 매니저 없이 브라우저 더블클릭만으로 실행되는 실행 모델. [[sans-kids-school-2025]]의 기반 아키텍처.
- Canvas API + 인라인 `<script>` + CDN 라이브러리만 허용. Node.js·npm·React·데이터베이스 등 금지.

## 왜 중요한가
- 파일럿 환경은 [[code-server]] 위의 브라우저 VS Code지만, **실행 preview는 저장 → 자동 새로고침 → 10초 내 시각 확인** 루프여야 한다. 빌드 단계가 없어야 이 루프가 가능.
- 에러 하나가 전체 빌드를 죽이지 않는다 → [[no-debug-philosophy]] 구현이 쉬워진다.
- 아이가 집에서도 `.html` 파일만 있으면 재실행할 수 있어, 파일럿 종료 후 지속 학습의 허들이 낮다.
- 백업 시나리오 단순: 네트워크·서버 장애 시에도 로컬 HTML 더블클릭 fallback이 가능 (`workshop-materials/offline-backup/`).

## 구성 요소 / 규칙
- **1 파일**: `<!DOCTYPE html>` + `<style>` + `<canvas>` + `<script>` 모두 인라인.
- **기본 캔버스**: 800×400px.
- **표준 게임 객체**: `hero`, `enemies`, `projectiles`, `gameState` 네 개로 대부분 커버.
- **방어적 렌더링**: 모든 draw 함수는 try-catch로 감싸고 기본값 객체를 전제한다 ([[no-debug-philosophy]] 참고).
- **허용**: Canvas, 인라인 스타일, CDN 라이브러리(중급에서 p5.js).
- **금지**: 빌드 도구, 별도 에셋 파일, 서버 기능, 복잡 프레임워크, DB.

## 파일럿 적용 포인트
- 게임 스타터 템플릿([[pilot-game-starter-template]])은 이 모델을 따라 만든다. 기존 자산 `sans-kids-school-2025/sandbox-environments/game-template-starter.html`을 시작점으로 활용 가능.
- [[code-server]] 세션의 Live Preview 확장과 단일 HTML 저장-리프레시 루프의 궁합을 리허설([[pilot-rehearsal-late-april]]) 시 반드시 확인한다.
- AI 튜터([[cline]])가 생성하는 코드가 이 규칙을 깨지 않도록 시스템 프롬프트에 "단일 HTML, 외부 파일·빌드 도구 금지" 규칙을 명시한다.

## 예시
```html
<!DOCTYPE html><html><body>
<canvas id="game" width="800" height="400"></canvas>
<script>
const ctx = document.getElementById('game').getContext('2d');
const hero = { x: 100, y: 300, size: 50, color: '#3498db' };
function draw(){ try{
    ctx.fillStyle = hero.color;
    ctx.fillRect(hero.x, hero.y, hero.size, hero.size);
}catch(e){ /* stay silent */ } }
requestAnimationFrame(function loop(){ draw(); requestAnimationFrame(loop); });
</script></body></html>
```

## 관련
- [[sans-kids-school-2025]] · [[no-debug-philosophy]] · [[pilot-game-starter-template]] · [[code-server]]
- 원본: `.raw/sans-kids-2025/CLAUDE.md`, `.raw/sans-kids-2025/README.md`
