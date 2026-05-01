# E2E 테스트 가이드

## 전제조건

- `src/backend/.env.local` 존재 + `GEMINI_API_KEY` 설정됨
- `MOCK_LLM=0` (실제 API 호출)
- Docker Desktop 실행 중 (방법 A) 또는 `uv`, `npm` 설치됨 (방법 B)

---

## 실행 방법

### A. Docker Compose (권장 — 프론트엔드까지 통합 확인)

```bash
# 프로젝트 루트에서
docker compose up -d --build
```

첫 빌드는 5분 내외 소요. 완료 확인:

```bash
docker compose ps
```

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | http://localhost:3000 |
| 백엔드 API | http://localhost:8000 |
| Langfuse 관측성 | http://localhost:3002 |

### B. 로컬 직접 실행 (빠른 확인)

```bash
# 터미널 1 — 백엔드
cd src/backend
uv run uvicorn main:app --reload --port 8000

# 터미널 2 — 프론트엔드
cd src/frontend
npm run dev
```

---

## 골든 패스 체크리스트

http://localhost:3000 접속 후 순서대로 확인.

로그인 정보: `admin` / `.env.local`의 `ADMIN_PASSWORD`

| # | 입력 | 기대 결과 | 확인 |
|---|------|-----------|------|
| 1 | 어드민 로그인 | 채팅 화면 진입 | ☐ |
| 2 | "토끼 캐릭터 만들어줘" | 카드 이미지 + 💡 힌트 표시 | ☐ |
| 3 | "별 모으기 게임 만들어줘" | iframe에 게임 로딩 | ☐ |
| 4 | "더 빠르게 해줘" | 같은 캐릭터로 속도 증가, **코드 채팅 노출 없음** | ☐ |
| 5 | "안녕!" | 텍스트 응답만, 게임·카드 이벤트 없음 | ☐ |

---

## 신규 기능 중점 확인

### edit_code_node (실 API 첫 검증)
- 게임 편집 시 Gemini `with_structured_output()` 사용
- 수정된 HTML 전체 반환, 코드 블록이 채팅창에 흘러나오지 않아야 함
- 캐릭터 SVG가 편집 후에도 그대로 유지되어야 함

### summarize_turn_node (실 API 첫 검증)
- 매 턴 종료 후 200자 이내 한국어 요약 생성
- 다음 턴에서 "그거 더 빠르게" 같은 전 턴 참조가 자연스럽게 처리되는지 확인

---

## 문제 발생 시

```bash
# 백엔드 로그 확인
docker compose logs backend -f

# 재빌드
docker compose up -d --build backend

# 전체 초기화 (Langfuse DB 포함 — API 키 재발급 필요)
docker compose down -v
docker compose up -d --build
```

Langfuse 관측성 확인: http://localhost:3002 → 프로젝트 → Traces
