"use client";

import { useEffect, useRef, useState } from "react";
import { useChat } from "@/hooks/useChat";
import PromptScaffold from "@/components/PromptScaffold";
import { SCAFFOLD_DATA } from "@/lib/scaffoldData";

interface ChatPaneProps {
  childId: string;
  sessionId: string;
  onGameReady: (gameUrl: string, gameHtml: string) => void;
  onLoadingChange?: (loading: boolean) => void;
  currentBlock: number;
  onBlockChange: (block: number) => void;
}

export default function ChatPane({
  childId,
  sessionId,
  onGameReady,
  onLoadingChange,
  currentBlock,
  onBlockChange,
}: ChatPaneProps) {
  const { messages, gameUrl, gameHtml, hint, isLoading, wsStatus, send } = useChat(
    childId,
    sessionId
  );
  const [input, setInput] = useState("");
  const [waitingMessage, setWaitingMessage] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 게임 URL/HTML 변경 시 부모에 전달
  useEffect(() => {
    if (gameUrl) onGameReady(gameUrl, gameHtml);
  }, [gameUrl, gameHtml, onGameReady]);

  // 로딩 상태 변경 시 부모에 전달
  useEffect(() => {
    onLoadingChange?.(isLoading);
  }, [isLoading, onLoadingChange]);

  // 새 메시지 도착 시 스크롤 최하단
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 대기 중 중간 피드백 타이머
  useEffect(() => {
    if (!isLoading) {
      setWaitingMessage(null);
      return;
    }
    const t1 = setTimeout(
      () => setWaitingMessage("AI가 열심히 생각하고 있어... 잠깐만 기다려봐! 💭"),
      15_000
    );
    const t2 = setTimeout(
      () => setWaitingMessage("거의 다 됐어! 조금만 더 기다려봐 🎮"),
      40_000
    );
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [isLoading]);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;
    send(input.trim());
    setInput("");
  };

  const handleQuickSend = (text: string) => {
    if (!text.trim() || isLoading) return;
    send(text.trim());
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* WS 재연결 상태 배너 */}
      {wsStatus !== "connected" && (
        <div
          className={`flex items-center justify-center gap-2 px-3 py-1.5 text-xs font-medium ${
            wsStatus === "reconnecting"
              ? "bg-yellow-900/80 text-yellow-300"
              : "bg-red-900/80 text-red-300"
          }`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              wsStatus === "reconnecting"
                ? "bg-yellow-400 animate-pulse"
                : "bg-red-400"
            }`}
          />
          {wsStatus === "reconnecting"
            ? "연결 중... 잠깐만 기다려봐 🔄"
            : "서버 연결이 끊겼어. 새로고침 해봐! ⚠️"}
        </div>
      )}
      {/* 블록 진행 표시 */}
      <div className="flex flex-wrap gap-1 border-b border-gray-800 px-4 py-2">
        {SCAFFOLD_DATA.map(({ block, skill }) => (
          <button
            key={block}
            onClick={() => onBlockChange(block)}
            title={skill}
            className={`flex-shrink-0 rounded px-2 py-1 text-xs font-medium transition-colors whitespace-nowrap ${
              block === currentBlock
                ? "bg-indigo-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            <span className="sm:hidden">{block + 1}</span>
            <span className="hidden sm:inline">{block + 1} {skill}</span>
          </button>
        ))}
      </div>

      {/* 블록별 프롬프트 스캐폴딩 카드 */}
      <PromptScaffold currentBlock={currentBlock} onSelect={handleQuickSend} />

      {/* 메시지 목록 */}
      <div className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.length === 0 && (
          <p className="text-center text-sm text-gray-600 mt-8">
            AI에게 만들고 싶은 게임을 말해봐! 👇
          </p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm ${
                msg.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-gray-800 text-gray-100"
              } ${msg.isStreaming ? "animate-pulse" : ""}`}
            >
              {/* 게임 HTML 제외하고 텍스트만 표시 */}
              {msg.text
                .replace(/```html[\s\S]*?```/gi, "")   // HTML 코드블록 제거
                .replace(/\n*💡[^\n]*$/m, "")           // 마지막 💡 힌트 줄 제거 (별도 버튼으로 표시)
                .trim() ||
                (msg.isStreaming ? "..." : "")}
            </div>
          </div>
        ))}
        {/* 대기 피드백 — 15초·40초 후 안심 메시지 */}
        {waitingMessage && isLoading && (
          <div className="flex justify-center">
            <p className="rounded-full bg-indigo-950 border border-indigo-800 px-4 py-1.5 text-xs text-indigo-300 animate-pulse">
              {waitingMessage}
            </p>
          </div>
        )}
        {/* 생각 중 dots — 로딩 중이고 아직 AI 응답이 없을 때 */}
        {isLoading && messages[messages.length - 1]?.role !== "assistant" && (
          <div className="flex justify-start">
            <div className="flex items-center gap-1 rounded-2xl bg-gray-800 px-4 py-3">
              {[0, 200, 400].map((delay) => (
                <span
                  key={delay}
                  className="h-2 w-2 rounded-full bg-gray-400 animate-bounce"
                  style={{ animationDelay: `${delay}ms` }}
                />
              ))}
            </div>
          </div>
        )}
        {/* 💡 힌트 — 클릭하면 따옴표 안 텍스트를 즉시 전송 */}
        {hint &&
          (() => {
            const match = hint.match(/"([^"]+)"/);
            const sendText = match
              ? match[1]
              : hint.replace(/^💡\s*/, "").trim();
            return (
              <button
                onClick={() => handleQuickSend(sendText)}
                disabled={isLoading}
                className="mx-auto block rounded-full border border-indigo-700 px-3 py-1 text-center text-xs text-indigo-400 hover:bg-indigo-950 disabled:opacity-50"
              >
                {hint}
              </button>
            );
          })()}
        <div ref={messagesEndRef} />
      </div>

      {/* 입력 영역 */}
      <div className="border-t border-gray-800 p-3">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isLoading ? "AI가 만들고 있어..." : "게임 설명을 입력해봐!"}
            disabled={isLoading}
            rows={2}
            className="flex-1 resize-none rounded-xl border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-gray-100 placeholder-gray-500 outline-none focus:border-indigo-500 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="self-end rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-500 disabled:opacity-40"
          >
            {isLoading ? "..." : "▶"}
          </button>
        </div>
      </div>
    </div>
  );
}
