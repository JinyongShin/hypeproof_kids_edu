/**
 * backendUrl.ts 단위 테스트
 *
 * 테스트 대상:
 *   1. getWsUrl — http/https → ws/wss 변환
 *   2. getBackendUrl — SSR vs 클라이언트 분기, window.__BACKEND_URL__ 오버라이드
 *
 * 실행:
 *   npm test  (또는 pnpm test)
 */

import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// ---------------------------------------------------------------------------
// 동적 import 헬퍼 — 모듈 수준 상수이므로 resetModules 후 재import 필요
// ---------------------------------------------------------------------------

async function importBackendUrl() {
  const mod = await import("../lib/backendUrl");
  return mod;
}

// ---------------------------------------------------------------------------
// 1. getWsUrl — HTTP → WebSocket 스킴 변환
// ---------------------------------------------------------------------------

describe("BACKEND_WS_URL — HTTP → WS 변환", () => {
  afterEach(() => {
    vi.resetModules();
    vi.unstubAllEnvs();
    // window.__BACKEND_URL__ 초기화
    delete (window as any).__BACKEND_URL__;
  });

  it("http:// URL 은 ws:// 로 변환된다", async () => {
    vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "http://localhost:8000");
    const { BACKEND_WS_URL } = await importBackendUrl();
    expect(BACKEND_WS_URL).toBe("ws://localhost:8000");
  });

  it("https:// URL 은 wss:// 로 변환된다", async () => {
    vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "https://example.trycloudflare.com");
    const { BACKEND_WS_URL } = await importBackendUrl();
    expect(BACKEND_WS_URL).toBe("wss://example.trycloudflare.com");
  });

  it("base 가 빈 문자열이면 빈 문자열을 반환한다", async () => {
    // 환경변수 없음, window.__BACKEND_URL__ 없음 → base = ""
    const { BACKEND_WS_URL } = await importBackendUrl();
    expect(BACKEND_WS_URL).toBe("");
  });

  it("window.__BACKEND_URL__ 이 http 이면 ws 로 변환된다", async () => {
    vi.resetModules();
    (window as any).__BACKEND_URL__ = "http://tunnel.example.com";
    const { BACKEND_WS_URL } = await importBackendUrl();
    expect(BACKEND_WS_URL).toBe("ws://tunnel.example.com");
    delete (window as any).__BACKEND_URL__;
  });

  it("window.__BACKEND_URL__ 이 https 이면 wss 로 변환된다", async () => {
    vi.resetModules();
    (window as any).__BACKEND_URL__ = "https://secure-tunnel.example.com";
    const { BACKEND_WS_URL } = await importBackendUrl();
    expect(BACKEND_WS_URL).toBe("wss://secure-tunnel.example.com");
    delete (window as any).__BACKEND_URL__;
  });
});

// ---------------------------------------------------------------------------
// 2. getBackendUrl — 환경변수 + window 오버라이드
// ---------------------------------------------------------------------------

describe("BACKEND_HTTP_URL — 환경변수 및 오버라이드", () => {
  afterEach(() => {
    vi.resetModules();
    vi.unstubAllEnvs();
    delete (window as any).__BACKEND_URL__;
  });

  it("NEXT_PUBLIC_BACKEND_HTTP_URL 이 설정되면 해당 값을 사용한다", async () => {
    vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "http://custom-host:9000");
    const { BACKEND_HTTP_URL } = await importBackendUrl();
    expect(BACKEND_HTTP_URL).toBe("http://custom-host:9000");
  });

  it("window.__BACKEND_URL__ 이 환경변수보다 우선 적용된다", async () => {
    vi.resetModules();
    vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "http://env-value:8000");
    (window as any).__BACKEND_URL__ = "http://override-url:7777";
    const { BACKEND_HTTP_URL } = await importBackendUrl();
    expect(BACKEND_HTTP_URL).toBe("http://override-url:7777");
    delete (window as any).__BACKEND_URL__;
  });

  it("둘 다 없으면 빈 문자열을 반환한다 (jsdom 클라이언트 환경)", async () => {
    // window 있음, __BACKEND_URL__ 없음, 환경변수 없음
    const { BACKEND_HTTP_URL } = await importBackendUrl();
    expect(BACKEND_HTTP_URL).toBe("");
  });
});
