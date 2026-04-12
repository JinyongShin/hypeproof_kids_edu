---
type: decision
status: active
priority: 2
date: 2026-01-19
owner: "[[jay-lee]]"
context: "내부 지식 공유 포맷"
tags:
  - decision
  - operations
  - ai-friendly
created: 2026-04-12
updated: 2026-04-12
---

# 지식 공유는 Markdown / PDF

## 결정
- 내부 자료는 **Markdown(.md) 또는 PDF**로 공유. Notion 링크는 지양.

## 근거
- AI/LLM이 MD·PDF를 가장 잘 파싱 → 학습·리서치·자동화에 유리.
- 이 원칙이 이 볼트(Obsidian = MD 네이티브) 선택의 근거이기도 함.

## 대안 및 기각 이유
- Notion: 링크 공유는 되나 AI 학습 파이프라인에 불편.
- Google Docs: 포맷 추출 시 노이즈 ↑.

## 영향 범위
- 모든 자료·미팅 노트·마케팅 문서 대상.
- [[kiwon-nam]] 마케팅 전략 플랫폼 문서도 MD로 작성.

## 관련
- [[2026-01-19-meeting]] · [[ai-native-workflow]]
