"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatPane from "@/components/ChatPane";
import GamePreview from "@/components/GamePreview";
import SessionSidebar from "@/components/SessionSidebar";
import { useSwipe } from "@/hooks/useSwipe";

const BACKEND_HTTP_URL =
  process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000";

export default function Home() {
  const router = useRouter();
  const [childId, setChildId] = useState("");
  const [activeSessionId, setActiveSessionId] = useState("");
  const [gameUrl, setGameUrl] = useState("");
  const [currentBlock, setCurrentBlock] = useState(0);
  const [activePane, setActivePane] = useState<"chat" | "game">("chat");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ready, setReady] = useState(false);

  // 로그인 확인 + 세션 초기화
  useEffect(() => {
    const id = sessionStorage.getItem("child_id") ?? "";
    if (!id) {
      router.replace("/login");
      return;
    }
    setChildId(id);

    // 저장된 활성 세션 복원, 없으면 새 세션 생성
    const savedSession = sessionStorage.getItem("active_session_id") ?? "";
    if (savedSession) {
      setActiveSessionId(savedSession);
      setReady(true);
    } else {
      fetch(`${BACKEND_HTTP_URL}/sessions/${id}`, { method: "POST" })
        .then((r) => r.json())
        .then(({ session_id }) => {
          sessionStorage.setItem("active_session_id", session_id);
          setActiveSessionId(session_id);
          setReady(true);
        })
        .catch(() => setReady(true));
    }
  }, [router]);

  const handleSessionChange = useCallback((sessionId: string) => {
    setActiveSessionId(sessionId);
    sessionStorage.setItem("active_session_id", sessionId);
    setGameUrl("");
  }, []);

  const handleLogout = useCallback(() => {
    sessionStorage.clear();
    router.replace("/login");
  }, [router]);

  const handleGameReady = useCallback((url: string) => {
    setGameUrl(url);
  }, []);

  const { onTouchStart, onTouchEnd } = useSwipe({
    onSwipeLeft: () => setActivePane("game"),
    onSwipeRight: () => setActivePane("chat"),
  });

  if (!ready || !childId || !activeSessionId) {
    return (
      <div className="flex h-full items-center justify-center bg-gray-950 text-gray-400">
        로딩 중...
      </div>
    );
  }

  return (
    <div className="flex h-full bg-gray-950">
      {/* 사이드바 — 데스크탑 항상 표시, 모바일 오버레이 */}
      <div
        className={`
          fixed inset-y-0 left-0 z-30 transition-transform duration-200
          md:relative md:translate-x-0
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
      >
        <SessionSidebar
          childId={childId}
          activeSessionId={activeSessionId}
          onSessionChange={(id) => {
            handleSessionChange(id);
            setSidebarOpen(false);
          }}
          onLogout={handleLogout}
        />
      </div>

      {/* 모바일 사이드바 오버레이 배경 */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/50 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* 메인 영역 */}
      <div className="relative flex-1 overflow-hidden">
        {/* 모바일 사이드바 토글 버튼 */}
        <button
          className="md:hidden absolute top-3 left-3 z-10 rounded-full bg-gray-800/80 px-3 py-1.5 text-xs text-white backdrop-blur-sm"
          onClick={() => setSidebarOpen(true)}
        >
          ☰
        </button>

        {/* 슬라이딩 트랙: 모바일 200vw / 데스크탑 100% */}
        <div
          className={`flex h-full transition-transform duration-300 ease-in-out w-[200%] md:w-full ${
            activePane === "game"
              ? "-translate-x-1/2 md:translate-x-0"
              : "translate-x-0"
          }`}
          onTouchStart={onTouchStart}
          onTouchEnd={onTouchEnd}
        >
          {/* 채팅 영역: 모바일 50%(=100vw) / 데스크탑 40% */}
          <div className="w-1/2 md:w-2/5 h-full flex flex-col border-r border-gray-800 text-gray-100">
            <ChatPane
              childId={childId}
              sessionId={activeSessionId}
              onGameReady={handleGameReady}
              currentBlock={currentBlock}
              onBlockChange={setCurrentBlock}
            />
          </div>

          {/* 게임 프리뷰 영역: 모바일 50%(=100vw) / 데스크탑 flex-1 */}
          <div className="relative w-1/2 md:flex-1 h-full">
            <GamePreview gameUrl={gameUrl} />

            {/* 좌측 에지 스와이프 캡처 존 — iframe이 터치 이벤트를 소비하는 문제 우회 */}
            <div
              className="md:hidden absolute inset-y-0 left-0 w-10 z-20"
              onTouchStart={onTouchStart}
              onTouchEnd={onTouchEnd}
            />

            {/* 채팅 복귀 버튼 */}
            <button
              className="md:hidden absolute top-3 left-3 z-20 rounded-full bg-gray-900/70 px-3 py-1.5 text-xs text-white backdrop-blur-sm"
              onClick={() => setActivePane("chat")}
            >
              ← 채팅
            </button>
          </div>
        </div>

        {/* 모바일 전용 하단 pane 인디케이터 */}
        <div className="md:hidden absolute bottom-3 left-0 right-0 flex justify-center gap-2 z-10 pointer-events-none">
          <div
            className={`w-2 h-2 rounded-full transition-colors duration-200 ${
              activePane === "chat" ? "bg-indigo-400" : "bg-gray-600"
            }`}
          />
          <div
            className={`w-2 h-2 rounded-full transition-colors duration-200 ${
              activePane === "game" ? "bg-indigo-400" : "bg-gray-600"
            }`}
          />
        </div>
      </div>
    </div>
  );
}
