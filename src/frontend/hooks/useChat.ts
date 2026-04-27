"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export interface Message {
  role: "user" | "assistant";
  text: string;
  isStreaming: boolean;
}

interface UseChatReturn {
  messages: Message[];
  cardUrl: string;
  cardJson: string;
  hint: string;
  isLoading: boolean;
  wsStatus: "connected" | "reconnecting" | "disconnected";
  send: (prompt: string) => void;
  stop: () => void;
  getLastUserMessage: () => string;
}

const BACKEND_WS_URL =
  process.env.NEXT_PUBLIC_BACKEND_WS_URL ?? "ws://localhost:8000";
const BACKEND_HTTP_URL =
  process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000";

export function useChat(childId: string, sessionId: string): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [cardUrl, setCardUrl] = useState("");
  const [cardJson, setCardJson] = useState("");
  const [hint, setHint] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [wsStatus, setWsStatus] = useState<"connected" | "reconnecting" | "disconnected">("connected");

  const wsRef = useRef<WebSocket | null>(null);

  // 세션 전환 시 히스토리 복원
  useEffect(() => {
    if (!childId || !sessionId) return;
    setIsLoading(false);
    setCardUrl("");
    setCardJson("");
    setHint("");
    setMessages([]);
    fetch(`${BACKEND_HTTP_URL}/sessions/${childId}/${sessionId}/messages`)
      .then((r) => (r.ok ? r.json() : []))
      .then((msgs: { role: "user" | "assistant"; text: string }[]) => {
        setMessages(msgs.map((m) => ({ ...m, isStreaming: false })));
      })
      .catch(() => {});
  }, [childId, sessionId]);

  useEffect(() => {
    if (!sessionId) return;

    let intentionallyClosed = false;
    let retryCount = 0;
    const MAX_RETRIES = 3;
    let retryTimer: ReturnType<typeof setTimeout> | null = null;

    function connect() {
      const ws = new WebSocket(
        `${BACKEND_WS_URL}/ws/chat/${childId}?session_id=${sessionId}`
      );
      wsRef.current = ws;

      ws.onopen = () => {
        setWsStatus("connected");
      };

      ws.onmessage = (event) => {
        retryCount = 0; // 메시지 수신 시 재시도 카운트 초기화
        setWsStatus("connected");
        const data = JSON.parse(event.data) as {
          type: "text" | "card" | "done" | "error";
          chunk?: string;
          card_url?: string;
          card_json?: string;
          hint?: string;
          session_id?: string;
        };

        if (data.type === "text" && data.chunk) {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant" && last.isStreaming) {
              return [
                ...prev.slice(0, -1),
                { ...last, text: last.text + data.chunk },
              ];
            }
            return [
              ...prev,
              { role: "assistant", text: data.chunk!, isStreaming: true },
            ];
          });
        } else if (data.type === "card" && data.card_url) {
          setCardUrl(data.card_url);
          if (data.card_json) setCardJson(data.card_json);
        } else if (data.type === "done") {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last?.role === "assistant") {
              return [...prev.slice(0, -1), { ...last, isStreaming: false }];
            }
            return prev;
          });
          if (data.hint) setHint(data.hint);
          if (data.card_url) setCardUrl(data.card_url);
          setIsLoading(false);
        } else if (data.type === "error") {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              text: `⚠️ ${data.chunk ?? "오류가 발생했어"}`,
              isStreaming: false,
            },
          ]);
          setIsLoading(false);
        }
      };

      ws.onerror = () => {
        setIsLoading(false);
      };

      ws.onclose = () => {
        if (intentionallyClosed) return;
        if (retryCount < MAX_RETRIES) {
          retryCount++;
          setWsStatus("reconnecting");
          retryTimer = setTimeout(connect, 1500);
        } else {
          setWsStatus("disconnected");
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              text: "⚠️ 서버 연결이 끊겼어. 잠깐 기다렸다 다시 해봐!",
              isStreaming: false,
            },
          ]);
          setIsLoading(false);
        }
      };
    }

    connect();

    return () => {
      intentionallyClosed = true;
      if (retryTimer) clearTimeout(retryTimer);
      wsRef.current?.close();
    };
  }, [childId, sessionId]);

  const send = useCallback(
    (prompt: string) => {
      if (!prompt.trim() || isLoading || !wsRef.current) return;
      if (wsRef.current.readyState !== WebSocket.OPEN) return;

      setMessages((prev) => [
        ...prev,
        { role: "user", text: prompt, isStreaming: false },
      ]);
      setHint("");
      setIsLoading(true);

      wsRef.current.send(JSON.stringify({ prompt }));
    },
    [isLoading]
  );

  const stop = useCallback(() => {
    wsRef.current?.close();
    setIsLoading(false);
  }, []);

  const getLastUserMessage = useCallback(() => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === "user") return messages[i].text;
    }
    return "";
  }, [messages]);

  return { messages, cardUrl, cardJson, hint, isLoading, wsStatus, send, stop, getLastUserMessage };
}
