---
type: analysis
topic: qa-agent-integration
date: 2026-04-27
author: AB_kimi_bot (subagent)
status: analysis-complete
updated: 2026-05-14
created: 2026-04-27
tags:
  - validation
  - qa
---

# game_forge QA 에이전트 분석 — 진용님 버전 연동 가능성 리포트

## 1. 개요

봉호님(Tae Bongho)의 game_forge QA 에이전트(`qa.py`)와 진용님 버전(`genai_runner.py` 기반)의 연동 가능성을 분석.

## 2. game_forge qa.py 현황

### 파일 탐색 결과
- `/Users/ryan/.openclaw/workspace/lessons/hypeproof_kids_edu/` 전체 탐색 결과: **`qa.py` 파일 없음**
- `game_forge` 디렉토리 또는 관련 Python 파일 **존재하지 않음**
- vault 문서, 미팅 노트에 game_forge/qa.py 관련 언급 **없음**

### 결론
봉호님의 game_forge QA 에이전트 코드는 아직 이 저장소에 통합되지 않았음. 별도 리포지토리 또는 로컬 환경에 있을 가능성.

## 3. 진용님 버전 (genai_runner.py) 아키텍처 분석

### 현재 구조
```
genai_runner.py
├── generate_card(prompt, child_id, session_id) → AsyncGenerator[StreamEvent]
│   ├── GLM (z.ai) 1차 시도
│   ├── Pollinations.ai 2차 폴백
│   ├── JSON 카드 추출 (_extract_card_json)
│   └── 카드 저장 (_save_card)
├── generate_image(image_prompt) → (bytes, mime_type)
├── StreamEvent (dataclass)
│   ├── type: text | card | image | done | error
│   ├── card_json, card_url, hint 등
│   └── 세션/카드 관리 포함
└── _save_card → storage 모듈 연동
```

### 핵심 특징
1. **LLM 백엔드**: GLM-5 (z.ai) + Pollinations.ai 폴백
2. **스트리밍**: AsyncGenerator 기반 이벤트 스트림
3. **카드 관리**: JSON 카드 추출 → 디스크 저장 → URL 생성
4. **세션 관리**: child_id + session_id 기반, 세션당 최대 10개 카드
5. **경로 보안**: 경로 순회 공격 방지 (`is_relative_to` 검증)

### QA 검증 포인트 (현재 없음)
- **카드 품질 검증**: card_type, 필수 필드 누락 체크 없음
- **응답 품질 검증**: 한국어, 아이 친화적 톤 체크 없음
- **컨텐츠 가이드라인**: 안전성/적절성 필터 없음
- **에러 핸들링**: LLM 실패 시 폴백만 있고, 카드 내용 검증 없음

## 4. 연동 가능성 분석

### 시나리오 A: qa.py를 미들웨어로 통합
```
generate_card() → [QA Agent] → StreamEvent
                    ├── 카드 품질 검증
                    ├── 응답 톤 체크
                    ├── 안전성 필터
                    └── 통과/수정요청 반환
```

**장점**: 기존 코드 변경 최소화  
**단점**: 응답 시간 증가 (현재 평균 20s + QA 시간)

### 시나리오 B: qa.py를 후처리 파이프라인으로 통합
```
generate_card() → 카드 저장 후 → [QA Agent] → 통과/수정
                                    ├── 카드 검증
                                    └── 필요시 재생성 트리거
```

**장점**: 실시간 응답 영향 없음  
**단점**: 사용자가 미검증 카드를 일시적으로 봄

### 시나리오 C: genai_runner 내부에 QA 로직 내장
```python
# generate_card 내부
card_json = _extract_card_json(full_text)
if card_json and _qa_validate(card_json):  # ← QA 로직
    _save_card(...)
else:
    # 재시도 또는 수정
```

**장점**: 가장 단순한 구현  
**단점**: genai_runner 책임 증가

## 5. 권장 연동 방안

### Phase 1: QA 인터페이스 정의 (봉호님 코드 수령 후)
```python
# qa_interface.py (제안)
class QAResult:
    passed: bool
    issues: list[str]
    fixed_card_json: str | None  # 자동 수정 시

async def validate_card(card_json: str, context: dict) -> QAResult:
    """카드 품질 검증"""
    ...
```

### Phase 2: genai_runner에 QA 훅 삽입
- `_extract_card_json` 이후, `_save_card` 이전에 QA 검증 삽입
- 실패 시 최대 1회 재시도
- QA 검증 결과 로깅

### Phase 3: 대시보드/모니터링
- QA 통과율 추적
- 자주 실패하는 패턴 분석

## 6. 차단 요소 및 액션 아이템

| # | 항목 | 상태 | 액션 |
|---|------|------|------|
| 1 | 봉호님 qa.py 코드 수령 | ❌ 미수령 | 봉호님에게 코드 공유 요청 |
| 2 | QA 검증 기준 합의 | ❌ 미정 | card_type별 필수 필드, 품질 기준 회의 |
| 3 | 응답 시간 영향 평가 | ❌ 미측정 | QA 로직 프로토타입 후 벤치마크 |
| 4 | 안전성 필터 요구사항 | ❌ 미정 | kids_edu 콘텐츠 가이드라인 확정 필요 |

## 7. 결론

**연동 가능성: 높음** — 구조적으로 QA 에이전트 삽입 포인트가 명확함.  
**차단 요소: 봉호님 코드 미수령** — qa.py가 이 저장소에 없어 구체적 연동 설계 불가.

### 즉시 가능한 작업
- genai_runner.py에 QA 훅 인터페이스(abstract) 추가
- 카드 품질 기준 문서화
- QA 결과 스키마 정의

### 봉호님 코드 수령 후 가능한 작업
- 구체적 연동 구현
- E2E 테스트에 QA 검증 포함
- 응답 시간 벤치마크
