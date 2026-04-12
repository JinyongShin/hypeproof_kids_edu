"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export interface Message {
  role: "user" | "assistant";
  text: string;
  isStreaming: boolean;
}

interface UseChatReturn {
  messages: Message[];
  gameHtml: string;
  hint: string;
  isLoading: boolean;
  send: (prompt: string) => void;
}

const BACKEND_WS_URL = process.env.NEXT_PUBLIC_BACKEND_WS_URL ?? "ws://localhost:8000";

export function useChat(childId: string): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [gameHtml, setGameHtml] = useState("");
  const [hint, setHint] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);

  // WebSocket 연결 초기화
  useEffect(() => {
    const ws = new WebSocket(`${BACKEND_WS_URL}/ws/chat/${childId}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data) as {
        type: "text" | "game" | "done" | "error";
        chunk?: string;
        html?: string;
        hint?: string;
        session_id?: string;
      };

      if (data.type === "text" && data.chunk) {
        // 스트리밍 텍스트를 현재 assistant 메시지에 누적
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "assistant" && last.isStreaming) {
            return [
              ...prev.slice(0, -1),
              { ...last, text: last.text + data.chunk },
            ];
          }
          return [...prev, { role: "assistant", text: data.chunk!, isStreaming: true }];
        });
      } else if (data.type === "game" && data.html) {
        setGameHtml(data.html);
      } else if (data.type === "done") {
        // 스트리밍 종료
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "assistant") {
            return [...prev.slice(0, -1), { ...last, isStreaming: false }];
          }
          return prev;
        });
        if (data.hint) setHint(data.hint);
        setIsLoading(false);
      } else if (data.type === "error") {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: `⚠️ ${data.chunk ?? "오류가 발생했어"}`, isStreaming: false },
        ]);
        setIsLoading(false);
      }
    };

    ws.onerror = () => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "⚠️ 서버에 연결할 수 없어. 잠깐 기다렸다 다시 해봐!", isStreaming: false },
      ]);
      setIsLoading(false);
    };

    return () => {
      ws.close();
    };
  }, [childId]);

  const send = useCallback((prompt: string) => {
    if (!prompt.trim() || isLoading || !wsRef.current) return;
    if (wsRef.current.readyState !== WebSocket.OPEN) return;

    // 사용자 메시지 추가
    setMessages((prev) => [...prev, { role: "user", text: prompt, isStreaming: false }]);
    setHint("");
    setIsLoading(true);

    wsRef.current.send(JSON.stringify({ prompt }));
  }, [isLoading]);

  return { messages, gameHtml, hint, isLoading, send };
}
