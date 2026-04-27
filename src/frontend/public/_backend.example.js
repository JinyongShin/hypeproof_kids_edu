// 사용법: 이 파일을 _backend.js 로 복사한 뒤 URL을 실행 환경에 맞게 수정.
// _backend.js 는 .gitignore 됨 (Cloudflare quick tunnel은 재시작마다 URL 바뀜).
// backendUrl.ts 가 window.__BACKEND_URL__ 을 NEXT_PUBLIC_BACKEND_HTTP_URL 보다 우선 사용한다.
window.__BACKEND_URL__ = "http://localhost:8000";
