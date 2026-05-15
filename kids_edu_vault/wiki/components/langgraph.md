---
type: component
status: stub
title: "LangGraph"
created: 2026-05-15
updated: 2026-05-15
tags:
  - component
  - backend
  - llm
---

# LangGraph

LangChain의 StateGraph 기반 워크플로우 오케스트레이션 프레임워크. HypeProof Kids Edu 백엔드 핵심 컴포넌트.

## 채택 근거
[[adr-langgraph-gemini-backend]] 참조.

## 주요 개념
- **StateGraph**: 노드(함수)와 엣지(조건부 라우팅)로 구성된 비순환 그래프
- **EduSessionState**: 이 프로젝트에서 정의한 상태 TypedDict
- **AsyncSqliteSaver**: 세션 상태 영속화 (SQLite)

## 관련
- [[adr-langgraph-gemini-backend]] — 전환 ADR (9-노드 그래프 토폴로지)
- [[kids-edu-backend]] — 백엔드 컴포넌트 페이지
- [[gemini-2-5-flash]] — LLM 제공사
