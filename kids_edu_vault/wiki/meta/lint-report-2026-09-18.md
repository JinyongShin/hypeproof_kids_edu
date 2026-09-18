---
type: meta
title: "Lint Report 2026-09-18"
created: 2026-09-18
updated: 2026-09-18
status: developing
tags:
  - meta
  - lint
---

# Lint Report: 2026-09-18

**범위**: 2026-09-18 Chalk 관문 ingest 직후 점검. 신규 6 · 갱신 14 페이지 중심 + 볼트 전체 링크 스캔.

## Summary
- Pages scanned: **340** (`wiki/` + `curriculum_wiki/`)
- 신규 페이지가 만든 **깨진 링크: 0건** ✅
- 신규 페이지 **고아: 0건** ✅ (6/6 전부 인바운드 확보)
- 신규 페이지 프론트매터 필수 필드: **6/6 충족** ✅ (`ruling-*` 1건에 `title` 보강 후)
- 볼트 전체 깨진 링크 타깃: **18** — 전부 **이번 작업 이전부터 있던 것**
- 볼트 전체 고아 후보: **5**

## 이번 ingest 결과 (신규 6페이지)

| 페이지 | 인바운드 | 프론트매터 | 깨진 링크 |
|---|---:|---|---|
| [[chalk-pedagogy-gate]] | 12 | ✅ | 0 |
| [[chalk-studio-architecture]] | 10 | ✅ | 0 |
| [[chalk-entry-point-20260918]] | 9 | ✅ | 0 |
| [[chalk-instructor-field-reality]] | 5 | ✅ | 0 |
| [[pedagogy-gate-at-service-freeze]] | 8 | ✅ | 0 |
| [[ruling-pedagogy-gate-implementation]] | 10 | ✅ | 0 |

**고립된 새 페이지가 없다.** 여섯 페이지 모두 기존 [[chalk]]·[[chalk-requirements]]·[[chalk-implementation-status]]·[[curriculum-schema]]·[[lesson-plan-quality-checklist]]과 양방향으로 물려 있다.

## 이번 작업이 고치지 않은 기존 문제

> 아래는 **이번 ingest 이전부터 있던 것**이며 이 작업의 범위가 아니었다. 손대지 않았다.

- **깨진 링크 18종** — 대부분 미생성 스텁 참조. 별도 정리 과제
- **고아 후보 5종**
- **파일명 중복**: `_index` 18개(폴더별 인덱스, **의도된 것**. 위키링크는 `[[folder/_index|_index]]` 경로 지정으로 해소)

## 규약 예외 (기존 판정 유지)

- **파일명 `kebab-case`** — wiki-lint 기본값("Title Case")과 다르다. `kids_edu_vault/CLAUDE.md`가 **의도적 채택**으로 명시하므로 naming 항목은 false positive로 무시한다.

## Needs review

| # | 항목 | 비고 |
|---|---|---|
| 1 | `curriculum_wiki/` lint 1·3~12 | **여전히 미구현.** lint 2만 `hypeproof-studio` 쪽에 구현됐다 → [[ruling-pedagogy-gate-implementation]] |
| 2 | 깨진 링크 18종 정리 | 이번 범위 밖 |
| 3 | `_templates/ingest-ruling.md`에 `title` 필드 없음 | 이번에 수동 보강했다. 템플릿 자체 수정은 **하지 않았다** — 승인 사안 |

## Notes
자동 수정은 하지 않았다. 신규 페이지 1건의 `title` 보강만 적용했다.
