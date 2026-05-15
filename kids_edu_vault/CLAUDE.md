# HypeProof Kids Edu: LLM Wiki

Mode: C (Business / Project)
Purpose: HypeProof 유료 파일럿(2026-05-05, 소아암 병동 어린이 대상 AI 코딩 교육) 실행환경 설계·운영 지식베이스.
Owner: JY (신진용)
Created: 2026-04-12

## Structure

```
kids_edu_vault/
├── .raw/                      # 원본 소스 (immutable). ingest 전 드랍존. 수정 금지.
├── _templates/                # 노트 타입별 템플릿 (10종)
├── wiki/
│   ├── index.md               # 마스터 카탈로그
│   ├── log.md                 # 작업 로그 (추가 전용, 새 항목은 최상단)
│   ├── hot.md                 # ~500단어 최근 컨텍스트 캐시
│   ├── overview.md            # 볼트 전체 요약
│   ├── stakeholders/          # 사람·조직·의사결정자
│   ├── decisions/             # 단일 결정 + 근거·날짜 (ADR)
│   ├── deliverables/          # OKR·마일스톤·작업
│   ├── intel/                 # 외부 조사·현장 맥락
│   ├── comms/                 # 미팅·스레드 합성 요약
│   ├── specs/                 # 설계 문서 (복합 결정 묶음)
│   ├── components/            # 기술 스택 컴포넌트별 페이지
│   ├── runbooks/              # 배포·당일 운영 절차
│   ├── concepts/              # 조직 맥락 용어·프레임워크
│   ├── sources/               # wiki-ingest 소스 요약 페이지 (원본 1개 = 요약 1개)
│   ├── questions/             # wiki-query 답변 파일링 폴더 (지식 복리 누적)
│   ├── validation/            # QA·커리큘럼 검증 결과 로그
│   ├── projects/              # 비교육 사업 문서 (HYROX 등 외부 프로젝트)
│   └── assets/                # 디자인·콘텐츠 자산 버전 관리
└── CLAUDE.md                  # 이 파일
```

### 폴더 선택 가이드

| 기록할 내용 | 폴더 | 예 |
|---|---|---|
| 사람/조직 | `stakeholders/` | JY, Jay, TJ |
| 개별 결정 + 근거 | `decisions/` | 디스코드 사용, 미팅 시간 |
| 여러 결정의 집합 / 설계도 | `specs/` | 파일럿 실행환경 설계 |
| 기술 도구 하나 | `components/` | code-server, Caddy |
| 해야 할 일 / OKR | `deliverables/` | API Key 발급, 리허설 |
| 운영 절차 | `runbooks/` | 당일 배포, 장애 대응 |
| 조직/개발 용어 | `concepts/` | Mission Driven, 트랙 A/B |
| 외부 자료·현장 체크 | `intel/` | 병원 장소 정보 |
| 미팅 합성 요약 | `comms/` | 2026-01-05-meeting |
| 비교육 사업 문서 | `projects/` | HYROX 제안서, 외부 세션 |
| 디자인·콘텐츠 자산 | `assets/` | 16원칙 assets v0.1 |
| QA·검증 테스트 결과 | `validation/` | E2E 결과, 에지케이스 로그 |
| ingest 소스 요약 | `sources/` | wiki-ingest 자동 생성 — 직접 생성 금지 |
| 쿼리 응답 아카이브 | `questions/` | wiki-query 자동 파일링 |

## Conventions

- 모든 노트는 YAML frontmatter 필수: `type`, `status`, `created`, `updated`, `tags` (최소).
- Wikilink는 `[[Note Name]]` 형식. 파일명은 고유해야 하며 경로는 생략.
- `.raw/` 안의 원본은 절대 수정 금지.
- `wiki/index.md`는 마스터 카탈로그: ingest 때마다 갱신.
- `wiki/log.md`는 추가 전용: 과거 엔트리 수정 금지. 새 로그는 파일 **최상단**에 삽입.
- `wiki/hot.md`는 500단어 이내 캐시: 매 세션 끝·ingest 후 **완전히 덮어쓸 것**(저널 아님).
- 날짜는 `YYYY-MM-DD` 만 사용 (ISO datetime 금지).
- YAML 안의 wikilink는 반드시 따옴표: `- "[[Page]]"`.
- **파일명**: `kebab-case` 사용 (예: `my-page.md`). wiki-lint 스킬의 기본값인 "Title Case with spaces"와 다름 — 이 볼트는 kebab-case를 의도적으로 채택. lint 실행 시 naming convention 항목은 false positive로 무시.
- **_index.md 파일**: `status: navigational` 필드 사용. 콘텐츠 페이지와 다른 용도임을 명시.
- **sources/ 폴더**: wiki-ingest 스킬이 자동 관리. 직접 파일 생성 금지.
- **questions/ 폴더**: wiki-query 스킬이 자동 파일링. 직접 파일 생성 금지.

## Operations

- **Ingest**: `.raw/`에 원본 드랍 → "ingest [파일명]" 또는 `/wiki ingest <파일>`
- **Query**: 질문 → `/wiki-query` 또는 "what do you know about X" (hot → index → page 순)
- **Lint**: `/wiki-lint` → 깨진 링크·고아 페이지·frontmatter 누락 점검
- **Save**: `/save` → 대화/인사이트를 wiki에 구조화 노트로 저장
- **Archive**: 오래된 원본은 `.archive/` 로 이동하여 `.raw/`를 깨끗하게 유지

## 입력 자료 (프로젝트 루트)

프로젝트 루트(`D:\HypeProofLab\hypeproof_kids_edu\`)에 있는 문서들은 ingest 대상:
- `pilot-env-design-draft.md` — 파일럿 기술 브리핑
- `meeting_notes/*` — 주간 미팅·OKR
- `build_teams.md` — subagent 설계 지시서

필요 시 `.raw/`에 복사한 뒤 ingest. 원본은 그대로 둠.
