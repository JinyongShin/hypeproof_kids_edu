"use client";

import { useEffect, useState } from "react";

const BACKEND_HTTP_URL =
  process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000";

interface SessionItem {
  session_id: string;
  created_at: string;
  last_game_url: string;
}

interface SessionSidebarProps {
  childId: string;
  activeSessionId: string;
  onSessionChange: (sessionId: string, lastGameUrl: string) => void;
  onLogout: () => void;
}

function formatSessionLabel(sessionId: string): string {
  // session_id = "{child_id}_{YYYYMMDD_HHmmss}"
  const match = sessionId.match(/_(\d{8})_(\d{6})$/);
  if (!match) return sessionId;
  const [, date, time] = match;
  const hh = time.slice(0, 2);
  const mm = time.slice(2, 4);
  return `세션 ${hh}:${mm}`;
}

export default function SessionSidebar({
  childId,
  activeSessionId,
  onSessionChange,
  onLogout,
}: SessionSidebarProps) {
  const [sessions, setSessions] = useState<SessionItem[]>([]);

  const fetchSessions = async () => {
    try {
      const res = await fetch(`${BACKEND_HTTP_URL}/sessions/${childId}`);
      if (res.ok) {
        setSessions(await res.json());
      }
    } catch {
      // 네트워크 오류 무시
    }
  };

  useEffect(() => {
    fetchSessions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [childId]);

  const handleNewSession = async () => {
    try {
      const res = await fetch(`${BACKEND_HTTP_URL}/sessions/${childId}`, {
        method: "POST",
      });
      if (res.ok) {
        const { session_id } = await res.json();
        await fetchSessions();
        onSessionChange(session_id, "");
      }
    } catch {
      // 네트워크 오류 무시
    }
  };

  const handleDelete = async (sessionId: string) => {
    try {
      const res = await fetch(
        `${BACKEND_HTTP_URL}/sessions/${childId}/${sessionId}`,
        { method: "DELETE" }
      );
      if (res.ok) {
        const next = sessions.filter((s) => s.session_id !== sessionId);
        setSessions(next);
        if (sessionId === activeSessionId) {
          if (next.length > 0) {
            onSessionChange(next[0].session_id, next[0].last_game_url ?? "");
          } else {
            // 목록이 비면 새 세션 자동 생성
            handleNewSession();
          }
        }
      }
    } catch {
      // 네트워크 오류 무시
    }
  };

  return (
    <div className="flex h-full w-48 flex-col border-r border-gray-800 bg-gray-950 text-sm text-gray-200">
      {/* 헤더 */}
      <div className="border-b border-gray-800 px-3 py-3">
        <p className="font-semibold text-white">{childId}</p>
        <button
          onClick={onLogout}
          className="mt-1 text-xs text-gray-500 hover:text-red-400"
        >
          로그아웃
        </button>
      </div>

      {/* 세션 목록 */}
      <div className="flex-1 overflow-y-auto py-2">
        {sessions.map((s) => (
          <div
            key={s.session_id}
            className={`group flex cursor-pointer items-center justify-between px-3 py-2 transition-colors ${
              s.session_id === activeSessionId
                ? "bg-indigo-900 text-white"
                : "hover:bg-gray-800 text-gray-300"
            }`}
            onClick={() => onSessionChange(s.session_id, s.last_game_url ?? "")}
          >
            <span className="truncate text-xs">
              {formatSessionLabel(s.session_id)}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleDelete(s.session_id);
              }}
              className="ml-1 hidden text-gray-600 hover:text-red-400 group-hover:block"
              title="삭제"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {/* 새 세션 버튼 */}
      <div className="border-t border-gray-800 p-3">
        <button
          onClick={handleNewSession}
          className="w-full rounded-lg bg-indigo-700 py-2 text-xs font-medium text-white transition-colors hover:bg-indigo-600"
        >
          + 새 세션
        </button>
      </div>
    </div>
  );
}
