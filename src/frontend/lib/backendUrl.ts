// 런타임 백엔드 URL — 터널 URL이 바뀌어도 재빌드 불필요
// 빌드 타임 NEXT_PUBLIC_ 대신 이 파일을 사용하세요

function getBackendUrl(): string {
  if (typeof window === "undefined") return process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000";
  return (window as any).__BACKEND_URL__ ?? process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "";
}

function getWsUrl(): string {
  if (typeof window === "undefined") return process.env.NEXT_PUBLIC_BACKEND_WS_URL ?? "ws://localhost:8000";
  const base = (window as any).__BACKEND_URL__ ?? process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "";
  if (!base) return "";
  return base.replace(/^https/, "wss").replace(/^http/, "ws");
}

export const BACKEND_HTTP_URL = getBackendUrl();
export const BACKEND_WS_URL = getWsUrl();
