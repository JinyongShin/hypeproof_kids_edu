
# Obsidian 지식베이스 설정

아래 순서대로 실행해줘. 각 단계 완료 후 보고하고 다음으로 넘어가.

---

## Step 1: Skills 설치

mkdir -p .claude/skills

git clone --depth 1 https://github.com/kepano/obsidian-skills /tmp/kepano-skills
cp -r /tmp/kepano-skills/skills/* .claude/skills/
rm -rf /tmp/kepano-skills

git clone --depth 1 https://github.com/AgriciDaniel/claude-obsidian /tmp/claude-ob
cp -r /tmp/claude-ob/skills/* .claude/skills/
rm -rf /tmp/claude-ob

설치 후 ls .claude/skills/ 로 설치된 skill 목록을 확인하고 보고해줘.

---

## Step 2: Vault 구조 분석 및 CLAUDE.md 생성

현재 디렉토리(vault 루트)의 폴더 구조를 전부 탐색해.
분석이 끝나면 아래 내용을 포함한 CLAUDE.md를 루트에 생성해:

- 폴더별 용도와 컨벤션
- 설치된 각 skill의 이름과 어떤 상황에 사용하는지
- 파일 작성 시 따라야 할 Obsidian 마크다운 규칙
- wikilink 사용 원칙 ([[페이지명]] 형식)

---

## Step 3: 검증

설치 완료 후 아래를 확인하고 결과를 보고해:

1. ls .claude/skills/ — skill 목록
2. cat CLAUDE.md — 생성된 내용 확인
3. 사용 가능한 slash 커맨드 목록 (/wiki, /save, /wiki-query, /wiki-lint 등)