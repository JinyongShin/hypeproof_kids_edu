---
type: meta
status: active
created: 2026-05-15
updated: 2026-05-15
tags:
  - meta/dashboard
---

# Wiki Dashboard

볼트 건강 상태 대시보드. Obsidian Dataview 쿼리 모음.
Last lint: [[lint-report-2026-05-15]] (2026-05-15) — 9 critical, 14 warnings, 15 suggestions.

---

## Active Deliverables

```dataview
TABLE status, updated, file.link AS Page
FROM "wiki/deliverables"
WHERE status != "delivered" AND status != "navigational" AND status != "final"
SORT updated ASC
```

## Stale In-Progress Deliverables (not updated in 30+ days)

```dataview
TABLE status, updated
FROM "wiki/deliverables"
WHERE status = "in-progress" AND date(updated) < date(today) - dur(30 days)
SORT updated ASC
```

## Pages Missing Required Frontmatter

```dataview
TABLE file.link AS Page, status, created, updated
FROM "wiki"
WHERE !type OR !status OR !created OR !updated OR !tags
AND file.name != "_index"
SORT file.folder ASC
```

## Seed Pages (stale if updated > 30 days ago)

```dataview
TABLE status, updated, file.link AS Page
FROM "wiki"
WHERE status = "seed"
SORT updated ASC
```

## Recent Decisions (last 30 days)

```dataview
TABLE file.link AS Decision, status, updated
FROM "wiki/decisions"
WHERE date(updated) >= date(today) - dur(30 days)
AND file.name != "_index"
SORT updated DESC
```

## All Active ADRs

```dataview
TABLE status, updated
FROM "wiki/decisions"
WHERE type = "decision" AND status != "superseded" AND file.name != "_index"
SORT updated DESC
```

## Stakeholder Map

```dataview
TABLE file.link AS Stakeholder, status, updated
FROM "wiki/stakeholders"
WHERE file.name != "_index"
SORT file.name ASC
```

## Pages Updated This Week

```dataview
TABLE file.link AS Page, updated
FROM "wiki"
WHERE date(updated) >= date(today) - dur(7 days)
AND file.name != "_index"
SORT updated DESC
```

## Lint History

| Date | Report | Critical | Warnings | Suggestions |
|---|---|---|---|---|
| 2026-05-15 | [[lint-report-2026-05-15]] | 9 | 14 | 15 |
