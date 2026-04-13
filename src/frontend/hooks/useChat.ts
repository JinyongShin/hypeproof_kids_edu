"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export interface Message {
  role: "user" | "assistant";
  text: string;
  isStreaming: boolean;
}

interface UseChatReturn {
  messages: Message[];
  gameUrl: string;
  hint: string;
  isLoading: boolean;
  send: (prompt: string) => void;
}

const BACKEND_WS_URL =
  process.env.NEXT_PUBLIC_BACKEND_WS_URL ?? "ws://localhost:8000";

export function useChat(childId: string, sessionId: string): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [gameUrl, setGameUrl] = useState("");
  const [hint, setHint] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!sessionId) return;

    const ws = new WebSocket(
      `${BACKEND_WS_URL}/ws/chat/${childId}?session_id=${sessionId}`
    );
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data) as {
        type: "text" | "game" | "done" | "error";
        chunk?: string;
        game_url?: string;
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
      } else if (data.type === "game" && data.game_url) {
        setGameUrl(data.game_url);
      } else if (data.type === "done") {
        setMessages((prev) => {
          const last = prev[prev.length - 1];
          if (last?.role === "assistant") {
            return [...prev.slice(0, -1), { ...last, isStreaming: false }];
          }
          return prev;
        });
        if (data.hint) setHint(data.hint);
        if (data.game_url) setGameUrl(data.game_url);
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
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "⚠️ 서버에 연결할 수 없어. 잠깐 기다렸다 다시 해봐!",
          isStreaming: false,
        },
      ]);
      setIsLoading(false);
    };

    return () => {
      ws.close();
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

  return { messages, gameUrl, hint, isLoading, send };
}
