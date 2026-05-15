---
type: runbook
title: "LLM Pulse — 16원칙·4주코스 업데이트 워크플로우"
status: active
owner: "봉호 태"
created: 2026-05-11
updated: 2026-05-11
tags:
  - runbook
  - intel
  - pulse
  - automation
related:
  - "[[assets_v0.1]]"
  - "[[one-track-multi-skin]]"
  - "[[curriculum-core]]"
---

# LLM Pulse — 16원칙·4주코스 업데이트 워크플로우

> **전제**: 4주 코스는 우리 프로덕트, 16원칙은 베이스. 두 자산은 **AI 발전 속도에 맞춰 살아 있어야 함**. 매일 외부 신호를 흡수해 vault에 반영하는 루프.

---

## 출력 (Single Source of Truth)

매 실행은 `wiki/intel/llm-pulse/YYYY-MM-DD.md` 1개 파일을 생성한다. 형식:

```markdown
---
type: pulse
date: 2026-05-12
sources: [geeknews, linkedin-정구봉, x-boris, ...]
---

# Pulse 2026-05-12

## 🚨 영향 (Action Items)
- 원칙 N **약화** — 근거: <link> · 제안: <one-liner>
- 4주 코스 WEEK 3 — 다중 모델 조율 활용 사례 추가: <link>

## 📰 오늘의 신호 (Raw)
- [geeknews] <title> · <one-line summary> · <link>
- [linkedin] <정구봉 글 요약> · <link>
- [x-boris] <tweet 요약> · <link>

## 🧭 분류
| 신호 | 영향 원칙 | 영향 주차 | 비고 |
|---|---|---|---|
| ... | 7,8 | W1 | 약화 신호 |
```

분류는 **assets_v0.1의 16원칙 번호(0–15)** 기준.

---

## 소스 정의

| ID | 소스 | 수집 방법 | 빈도 |
|---|---|---|---|
| `geeknews` | https://news.hada.io | RSS: `https://feeds.hada.io/rss/news` | 일 1회 |
| `linkedin-정구봉` | LinkedIn / 정구봉 프로필 글 | LinkedIn 공식 API 없음 → `mcp__fetch__fetch` + 정구봉 URL 수동 등록 (`config/sources.yaml`) | 일 1회 |
| `x-boris` | X(Twitter) Boris 계정 (URL 봉호 확정 필요) | `mcp__fetch__fetch` + nitter mirror 또는 X API | 일 1회 |
| `+추가` | 새 소스는 `config/sources.yaml`에 한 줄 추가만으로 등록 | — | — |

**확정 필요한 입력 (봉호님)**
1. LinkedIn 정구봉 프로필 URL
2. X Boris 계정 핸들 (예: `@borismpower` 등)
3. 추가 소스 (예: Latent Space, Stratechery, Lex Fridman, Anthropic blog 등) — 자유 추가

---

## 처리 파이프라인

```
[1] FETCH      → 소스별 raw 항목 수집 (24h 윈도우)
[2] DEDUPE     → 어제 pulse와 중복 제거 (URL 해시)
[3] SUMMARIZE  → 항목당 한 줄 요약 (Gemini/Claude flash 모드)
[4] CLASSIFY   → 16원칙 매핑 + 4주코스 영향 (LLM judge)
[5] WRITE      → wiki/intel/llm-pulse/YYYY-MM-DD.md 생성
[6] HOT-UPDATE → 영향도 ≥ MEDIUM 항목이 있으면 hot.md "최근 시그널" 섹션 갱신
[7] DELIVER    → 텔레그램 다이제스트 (3줄 핵심 + PDF 파일 경로)
```

각 단계는 OpenClaw 스킬로 매핑:
- [1] `mcp__fetch__fetch` + `openclaw-skills:blogwatcher` (RSS)
- [3] `openclaw-skills:summarize` (Gemini 2.5 Flash 권장 — 가격/속도)
- [4] `openclaw-skills:gemini` 또는 Claude Haiku 4.5 (분류 only)
- [5] Write 도구
- [7] `openclaw message send --channel telegram`

---

## 분류 프롬프트 (Stage 4 핵심)

```
[입력] 1줄 요약 + 원문 링크
[출력 JSON] {
  "principles": [0–15 중 영향받는 번호 배열, 없으면 []],
  "weeks": [1–4 중 영향받는 주차 배열, 없으면 []],
  "impact": "HIGH|MEDIUM|LOW",
  "direction": "강화|약화|새 원칙 후보|컨텍스트 예시",
  "one_line_action": "이 신호를 vault에 어떻게 반영할지 한 줄"
}
```

LLM은 **assets_v0.1 16원칙 본문 + 4주 코스 구조**를 시스템 프롬프트로 받는다. 그래야 분류가 정확함.

---

## 실행 방법

### 수동 (검증용)
```bash
cd /home/taebh/.openclaw/hypeproof-workspace/tools/llm-pulse
./run.sh                    # 오늘 날짜 pulse 생성
./run.sh 2026-05-12         # 특정 날짜
./run.sh --dry-run          # 적재·전송 없이 콘솔만
```

### 자동 (cron, 매일 08:00 KST)
```
# 등록 명령 (봉호님 승인 후)
openclaw cron add \
  --name "llm-pulse-daily" \
  --schedule "0 23 * * *"  \
  --command "/home/taebh/.openclaw/hypeproof-workspace/tools/llm-pulse/run.sh" \
  --on-success "openclaw message send --channel telegram --target -5216727532 --message '✅ Pulse 적재됨'"
```
* cron은 UTC. 08:00 KST = 23:00 UTC (전날)

---

## 디렉토리 구조 (1차)

```
tools/llm-pulse/
├── run.sh                 # 엔트리 (단계 1~7 순차 실행)
├── config/
│   ├── sources.yaml       # 소스 등록 (URL·셀렉터·빈도)
│   └── prompts/
│       ├── summarize.md   # Stage 3 프롬프트
│       └── classify.md    # Stage 4 프롬프트 (assets_v0.1 임베드)
├── lib/
│   ├── fetch.py
│   ├── dedupe.py
│   ├── summarize.py
│   ├── classify.py
│   └── publish.py
└── cache/
    └── seen_urls.sqlite   # 중복 제거용
```

---

## 16원칙 자체 업데이트 트리거

`wiki/intel/llm-pulse/*.md`가 **30일간 누적**되면 자동 회고:
- 같은 원칙이 5회 이상 "약화" 분류 → 폐기 후보로 deprecation PR 생성
- "새 원칙 후보" 분류가 3회 이상 → `assets_v0.2` draft 생성

→ 16원칙은 정적인 문서가 아니라 **30일 윈도우로 자체 갱신**. 13 언러닝의 자동화.

---

## 다음 단계 (구현 순서)

- [ ] (1) sources.yaml 작성 — 봉호님 확정 URL 3개 입력 필요
- [ ] (2) `lib/` 스크립트 골격 작성 (200 LOC 내외 단일 파이프)
- [ ] (3) 1회 수동 실행 → 첫 pulse 파일 검증
- [ ] (4) cron 등록 (수동 검증 통과 후)
- [ ] (5) 텔레그램 다이제스트 포맷 봉호님 검증

---

## 관련

- [[assets_v0.1]] — 분류 기준
- [[curriculum-core]] · [[one-track-multi-skin]] — 4주 코스 베이스
- 30일 회고로 assets_v0.2 (미착수) 후보 자동 생성 예정
