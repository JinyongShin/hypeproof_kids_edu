---
type: concept
status: active
tags:
  - concept
  - pedagogy
  - ai-tutor
  - pilot
  - sans-kids
created: 2026-04-12
updated: 2026-04-12
---

# AI Persona Workflows (AI 튜터 5종 페르소나)

## 정의
- [[sans-kids-school-2025]]에서 검증한 AI 튜터의 5가지 교수법 페르소나. 각각 Cursor Rules 파일(`workflows/workflow-N/cursor-rules.md`)로 구현되어 있다.
- 한 명의 AI를 프롬프트 레이어에서 다른 선생님으로 "변신"시키는 설계.

## 왜 중요한가
- 동일한 코드 결과를 내더라도, 아이의 성향(창의형·분석형·성취형·사회형·체계형)에 따라 **몰입률**이 달라진다.
- 파일럿은 40명 8–12세를 동시에 다뤄야 하며 ([[environ-kukrip-amsenter]]), 정서 상태가 개별로 편차가 크다. 단일 페르소나로는 전원 몰입을 만들기 어렵다.
- [[fast-implementation-mode]] 결정과 결합하면, 페르소나는 말투·격려 방식을 담당하고 속도는 시스템 프롬프트가 담당하는 분업이 가능하다.

## 구성 요소 / 5종 페르소나
1. **Friendly Teacher (W1, 친절한 선생님)** — 격려·칭찬 중심, "~해볼까?" 제안형. 8–10세·사회형에게 fit.
2. **Problem-Solving Coach (W2, 문제해결 코치)** — 소크라테스식 역질문, 답 대신 단서. 11–13세·분석형에게 fit.
3. **Quick Implementation Helper (W3, 빠른 구현)** — 복붙 가능한 완성 코드 즉시 제공, 10분 단위 가시 결과. 14–16세·성취형에게 fit. → [[fast-implementation-mode]]의 원형.
4. **Storytelling Developer (W4, 스토리텔러)** — 코드를 "마법 주문"으로, 진행을 "퀘스트"로. 8–10세·창의형에게 fit. 병동 맥락에서 정서적으로 가장 안전.
5. **Checklist Method (W5, 체크리스트)** — 단계별 명시적 체크박스·시간 예산. 11–13세·체계형에게 fit.

## 파일럿 적용 포인트
- 병동 파일럿의 기본 페르소나는 **W3 변형(속도 우선) + W4 변형(스토리 래핑)**의 합성이 유력. [[combat-vs-cooperative-framing]] 결정에 따라 W4의 "악당·전투" 어휘는 협력형 어휘로 치환한다.
- 5종을 모두 탑재하되, 운영자가 아이를 관찰해 도중에 1회 스위칭할 수 있는 핫스왑 프롬프트를 준비한다.
- 페르소나 선택 가이드는 `.raw/sans-kids-2025/educational-scenarios/comprehensive-scenario-guide.md`의 decision tree(성향 관찰 5분 → 페르소나 할당)를 참고 재작성.

## 예시
- W1: "와! 날아다니는 원숭이라니 정말 멋진 아이디어야! 🚀"
- W2: "현실에서 우리가 움직일 때를 생각해봐. 왼쪽으로 가려면 뭘 해야 하지?"
- W3: "이 코드를 복사해서 붙여넣어봐. 실행하면 점프가 나타날 거야."
- W4: "영웅에게 '비행의 축복'을 내리고 싶구나! 🦅"
- W5: "✅ 체크: 하늘색 게임 화면이 보이는가? 10분 안에 완료!"

## 관련
- [[sans-kids-school-2025]] · [[fast-implementation-mode]] · [[no-debug-philosophy]] · [[cline]] · [[gemini-2-5-flash]]
- 원본: `.raw/sans-kids-2025/workflows/workflow-{1..5}/cursor-rules.md`, `.raw/sans-kids-2025/educational-scenarios/comprehensive-scenario-guide.md`
