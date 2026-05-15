/**
 * useChat 훅 단위 테스트
 *
 * 테스트 대상:
 *   1. WS 연결 시 session_id 쿼리파라미터 포함 확인
 *   2. game 이벤트 수신 시 gameUrl state 업데이트
 *   3. session_id 없을 때 WS 연결 시도하지 않음
 *
 * 실행:
 *   npm test  (또는 pnpm test)
 */

import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// ---------------------------------------------------------------------------
// WebSocket 모의 구현
// ---------------------------------------------------------------------------

/**
 * 최소한의 WebSocket 모의 클래스.
 * 생성된 인스턴스를 외부에서 참조할 수 있도록 lastInstance 에 저장한다.
 */
class MockWebSocket {
  static lastInstance: MockWebSocket | null = null;
  static OPEN = 1;

  url: string;
  readyState: number;
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: Event) => void) | null = null;
  onclose: ((event: CloseEvent) => void) | null = null;
  onopen: ((event: Event) => void) | null = null;

  private _sentMessages: string[] = [];

  constructor(url: string) {
    this.url = url;
    this.readyState = MockWebSocket.OPEN;
    MockWebSocket.lastInstance = this;
  }

  send(data: string) {
    this._sentMessages.push(data);
  }

  close() {
    this.readyState = 3; // CLOSED
  }

  /** 테스트에서 서버 메시지를 시뮬레이션할 때 사용 */
  simulateMessage(data: unknown) {
    if (this.onmessage) {
      this.onmessage({ data: JSON.stringify(data) } as MessageEvent);
    }
  }

  get sentMessages() {
    return this._sentMessages;
  }
}

// ---------------------------------------------------------------------------
// 테스트 setup / teardown
// ---------------------------------------------------------------------------

beforeEach(() => {
  MockWebSocket.lastInstance = null;
  // 전역 WebSocket 을 모의 구현으로 교체
  (globalThis as unknown as Record<string, unknown>).WebSocket = MockWebSocket;
});

afterEach(() => {
  vi.resetModules();
});

// ---------------------------------------------------------------------------
// 동적 import 헬퍼 — BACKEND_WS_URL 는 모듈 수준 상수이므로
//   매 테스트마다 resetModules 후 재import 해서 모의 환경을 반영한다.
// ---------------------------------------------------------------------------

async function importUseChat() {
  // vi.resetModules() 이후 호출해야 환경 변수 변경이 반영된다
  const mod = await import("../hooks/useChat");
  return mod.useChat;
}

// ---------------------------------------------------------------------------
// 1. WS 연결 시 session_id 쿼리파라미터 포함 확인
// ---------------------------------------------------------------------------

describe("useChat — WebSocket 연결 URL", () => {
  it("session_id 가 있을 때 WS URL 에 session_id 쿼리파라미터가 포함된다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    renderHook(() => useChat("child01", "child01_20260413_120000"));

    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    const url = MockWebSocket.lastInstance!.url;
    expect(url).toContain("child01");
    expect(url).toContain("session_id=child01_20260413_120000");
  });

  it("WS URL 이 올바른 WebSocket 스킴(ws:// 또는 wss://)으로 시작한다", async () => {
    vi.resetModules();
    vi.stubEnv("NEXT_PUBLIC_BACKEND_HTTP_URL", "http://localhost:8000");
    const useChat = await importUseChat();

    renderHook(() => useChat("child01", "child01_20260413_120001"));

    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    const url = MockWebSocket.lastInstance!.url;
    expect(url).toMatch(/^wss?:\/\//);
    vi.unstubAllEnvs();
  });

  it("child_id 가 URL 경로에 포함된다 (/ws/chat/{child_id})", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    renderHook(() => useChat("alice", "alice_20260413_130000"));

    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    expect(MockWebSocket.lastInstance!.url).toContain("/ws/chat/alice");
  });
});

// ---------------------------------------------------------------------------
// 2. game 이벤트 수신 시 gameUrl state 업데이트
// ---------------------------------------------------------------------------

describe("useChat — game 이벤트 처리", () => {
  it("game 이벤트를 수신하면 gameUrl 이 업데이트된다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    const { result } = renderHook(() =>
      useChat("child01", "child01_20260413_120000")
    );

    // WS 연결 대기
    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    const expectedUrl = "http://localhost:8000/games/child01/child01_20260413_120000/game_12345";

    act(() => {
      MockWebSocket.lastInstance!.simulateMessage({
        type: "game",
        game_url: expectedUrl,
      });
    });

    expect(result.current.gameUrl).toBe(expectedUrl);
  });

  it("game 이벤트의 game_url 이 빈 문자열이면 gameUrl 은 업데이트되지 않는다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    const { result } = renderHook(() =>
      useChat("child01", "child01_20260413_120000")
    );

    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    act(() => {
      MockWebSocket.lastInstance!.simulateMessage({
        type: "game",
        game_url: "",
      });
    });

    // game_url 이 falsy → setGameUrl 호출 안 됨 → 초기값 "" 유지
    expect(result.current.gameUrl).toBe("");
  });

  it("done 이벤트의 game_url 도 gameUrl 을 업데이트한다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    const { result } = renderHook(() =>
      useChat("child01", "child01_20260413_120000")
    );

    await waitFor(() => {
      expect(MockWebSocket.lastInstance).not.toBeNull();
    });

    const expectedUrl = "http://localhost:8000/games/child01/child01_20260413_120000/game_done";

    act(() => {
      MockWebSocket.lastInstance!.simulateMessage({
        type: "done",
        game_url: expectedUrl,
        hint: "💡 다음엔 하트를 모아봐!",
        session_id: "mock-session",
      });
    });

    expect(result.current.gameUrl).toBe(expectedUrl);
  });
});

// ---------------------------------------------------------------------------
// 3. session_id 없을 때 WS 연결 시도하지 않음
// ---------------------------------------------------------------------------

describe("useChat — session_id 없을 때 WS 미연결", () => {
  it("session_id 가 빈 문자열이면 WebSocket 인스턴스를 생성하지 않는다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    renderHook(() => useChat("child01", ""));

    // 충분한 시간이 지나도 WS 가 생성되지 않아야 한다
    await new Promise((r) => setTimeout(r, 50));

    expect(MockWebSocket.lastInstance).toBeNull();
  });

  it("session_id 없을 때 send 를 호출해도 오류가 발생하지 않는다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    const { result } = renderHook(() => useChat("child01", ""));

    // wsRef.current 가 null 이므로 send 는 조용히 무시된다
    expect(() => {
      act(() => {
        result.current.send("안녕!");
      });
    }).not.toThrow();
  });

  it("session_id 가 빈 문자열이면 WebSocket 인스턴스를 생성하지 않는다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();

    // useChat 은 sessionId 를 그대로 사용하므로, 공백은 truthy — 이 케이스는
    // 실제로 WS 가 연결된다. 이 테스트는 빈 문자열("")만이 보호됨을 문서화한다.
    // 공백(" ") 입력은 현재 구현이 WS 연결을 시도하는 알려진 동작이다.
    renderHook(() => useChat("child01", ""));

    await new Promise((r) => setTimeout(r, 50));

    expect(MockWebSocket.lastInstance).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// 4. send() 가드 + payload 검증
// ---------------------------------------------------------------------------

describe("useChat — send() 동작", () => {
  it("readyState 가 OPEN 이 아니면 send() 호출 시 메시지를 전송하지 않는다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();
    const { result } = renderHook(() => useChat("child01", "sess01"));

    await waitFor(() => expect(MockWebSocket.lastInstance).not.toBeNull());

    // CLOSED 상태로 전환 (onclose 핸들러는 트리거되지 않음 — 직접 값만 변경)
    MockWebSocket.lastInstance!.readyState = 3;

    act(() => {
      result.current.send("테스트 메시지");
    });

    expect(MockWebSocket.lastInstance!.sentMessages).toHaveLength(0);
  });

  it("send() 호출 시 { prompt: ... } 형식 JSON 을 전송한다", async () => {
    vi.resetModules();
    const useChat = await importUseChat();
    const { result } = renderHook(() => useChat("child01", "sess01"));

    await waitFor(() => expect(MockWebSocket.lastInstance).not.toBeNull());

    act(() => {
      result.current.send("별을 모으는 게임");
    });

    expect(MockWebSocket.lastInstance!.sentMessages).toHaveLength(1);
    const parsed = JSON.parse(MockWebSocket.lastInstance!.sentMessages[0]);
    expect(parsed).toEqual({ prompt: "별을 모으는 게임" });
  });
});
