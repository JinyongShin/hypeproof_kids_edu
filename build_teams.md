
당신은 지금부터 이 프로젝트의 개발을 위한 **subagent 팀을 직접 설계하고 생성**해야 합니다.

## 1단계: Skills 탐색 (필수 선행)

먼저 다음 위치에서 사용 가능한 skills를 전부 파악하세요:
- `~/.claude/skills/` (개인 skills)
- `.claude/skills/` (프로젝트 skills)
- `ls ~/.claude/skills/*/SKILL.md` 명령어로 발견

각 SKILL.md의 name과 description을 읽어 어떤 capabilities가 있는지 목록을 만드세요.

## 2단계: Subagent 설계 원칙

아래 원칙에 따라 subagent를 설계하세요:

**역할 분리**: 각 subagent는 단일 책임 원칙으로 설계 (하나의 역할만)
**Skills 활용**: 각 subagent의 `skills` frontmatter에 관련 skill을 명시적으로 preload
**Model 최적화**: 
  - 탐색/리서치용 → haiku (빠르고 저렴)
  - 구현/작성용 → sonnet (균형)
  - 아키텍처/복잡 판단 → inherit (메인과 동일)
**Tool 제한**: 역할에 맞게 tool을 최소한으로 제한
  - 읽기 전용 역할 → Read, Grep, Glob
  - 구현 역할 → Read, Write, Edit, Bash
  - 리서치 역할 → Read, Grep, Glob, WebFetch, WebSearch

## 3단계: 생성할 Subagent 목록 (프로젝트에 맞게 조정)

다음 subagent들을 `.claude/agents/` 폴더에 생성하세요:

### `architect.md`
- **역할**: 기능 요청을 받아 설계 문서(ADR)를 작성하고 구현 계획 수립
- **tools**: Read, Grep, Glob, Write
- **model**: inherit
- **skills**: 발견된 skills 중 아키텍처/문서 관련 skill 포함
- **description**: "Use when planning new features, major refactors, or system design decisions. Produces architecture decision records and implementation plans."

### `implementer.md`
- **역할**: architect의 계획을 받아 실제 코드를 구현
- **tools**: Read, Write, Edit, Bash, Glob, Grep
- **model**: sonnet
- **skills**: 발견된 skills 중 코딩/프레임워크 관련 skill 포함
- **description**: "Use when writing, editing, or generating code based on a spec or plan. Takes architecture decisions and implements them."

### `reviewer.md`
- **역할**: 코드 변경사항을 보안, 성능, 품질 관점에서 리뷰
- **tools**: Read, Grep, Glob (읽기 전용)
- **model**: sonnet
- **description**: "Use before commits or PRs to review code for security vulnerabilities, performance issues, and code quality. Always use proactively before merging."

### `debugger.md`
- **역할**: 버그 분석, 에러 트레이싱, 수정 방안 제시
- **tools**: Read, Grep, Glob, Bash
- **model**: sonnet
- **description**: "Use when encountering errors, failing tests, or unexpected behavior. Analyzes logs, traces issues, and proposes fixes."

### `tester.md`
- **역할**: 테스트 작성 및 실행, 커버리지 리포트
- **tools**: Read, Write, Edit, Bash
- **model**: sonnet
- **skills**: 발견된 skills 중 테스트 관련 skill 포함
- **description**: "Use when writing unit tests, integration tests, or running test suites. Generates test cases based on implementation."

### `docs-writer.md`
- **역할**: README, API 문서, 코드 주석 작성
- **tools**: Read, Grep, Glob, Write, Edit
- **model**: haiku
- **description**: "Use when creating or updating documentation, README files, API docs, or inline code comments."

## 4단계: CLAUDE.md 업데이트

`.claude/CLAUDE.md` (없으면 생성)에 다음을 추가하세요:

```
## Subagent 위임 원칙

이 프로젝트는 전문화된 subagent 팀으로 구성됩니다. 아래 상황에서 반드시 해당 subagent에게 위임하세요:

- **새 기능 설계** → @architect 먼저 호출
- **코드 구현** → @implementer에게 위임 (architect 계획이 있을 경우 계획 전달)
- **코드 리뷰** → @reviewer에게 위임 (커밋 전 필수)
- **버그/에러 발생** → @debugger에게 위임
- **테스트 작성** → @tester에게 위임
- **문서 작성** → @docs-writer에게 위임

메인 대화는 조율(orchestration)에 집중하고, 세부 탐색/구현은 subagent를 통해 context를 격리하세요.
개발 흐름: architect → implementer → tester → reviewer → docs-writer
```

## 5단계: 검증

모든 subagent 파일 생성 후:
1. `ls .claude/agents/` 로 파일 목록 확인
2. 각 파일의 frontmatter 문법 검증 (name, description, tools, model 필드)
3. skills preload가 올바르게 연결되어 있는지 확인
4. 간단한 테스트: "Use the architect agent to outline the approach for [첫 번째 기능]"

## 최종 리포트

생성 완료 후 다음을 보고하세요:
- 생성된 각 subagent 이름, 역할, 연결된 skills 목록
- 발견했지만 연결하지 않은 skills와 그 이유
- 이 프로젝트 특성에 맞게 조정한 사항
- 권장 개발 워크플로우 (어떤 순서로 어느 agent를 사용할지)

이제 시작하세요.

---

**과도한 subagent 방지**: subagent를 모든 것에 정의하고 싶은 유혹이 있지만, 너무 많은 specialist agent는 자동 위임을 덜 신뢰할 수 있게 만든다. 대부분의 팀은 잘 범위가 정해진 소수의 agent로 정착한다.