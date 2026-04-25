"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ChatPane from "@/components/ChatPane";
import CardPreview from "@/components/GamePreview";
import SessionSidebar from "@/components/SessionSidebar";
import { useSwipe } from "@/hooks/useSwipe";

const BACKEND_HTTP_URL =
  process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000";

export default function Home() {
  const router = useRouter();
  const [childId, setChildId] = useState("");
  const [activeSessionId, setActiveSessionId] = useState("");
  const [cardUrl, setCardUrl] = useState("");
  const [cardJson, setCardJson] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentBlock, setCurrentBlock] = useState(0);
  const [activePane, setActivePane] = useState<"chat" | "card">("chat");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [ready, setReady] = useState(false);
  const [sessionRefreshToken, setSessionRefreshToken] = useState(0);

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

  // activeSessionId 변경 시 최신 last_card_url fetch + isLoading 강제 리셋
  useEffect(() => {
    if (!childId || !activeSessionId) return;
    setIsLoading(false);
    fetch(`${BACKEND_HTTP_URL}/sessions/${childId}`)
      .then((r) => r.json())
      .then((sessions: { session_id: string; last_card_url: string }[]) => {
        const s = sessions.find((x) => x.session_id === activeSessionId);
        if (s?.last_card_url) setCardUrl(s.last_card_url);
      })
      .catch(() => {});
  }, [childId, activeSessionId]);

  const handleSessionChange = useCallback((sessionId: string, lastCardUrl: string) => {
    setActiveSessionId(sessionId);
    sessionStorage.setItem("active_session_id", sessionId);
    setCardUrl(lastCardUrl);
    setCardJson(""); // 세션 전환 시 JSON 초기화
  }, []);

  const handleLogout = useCallback(() => {
    sessionStorage.clear();
    router.replace("/login");
  }, [router]);

  const handleCardReady = useCallback((url: string, json: string) => {
    setCardUrl(url);
    setCardJson(json);
    setSessionRefreshToken((t) => t + 1);
  }, []);

  const { onTouchStart, onTouchEnd } = useSwipe({
    onSwipeLeft: () => setActivePane("card"),
    onSwipeRight: () => setActivePane("chat"),
  });

  if (!ready || !childId || !activeSessionId) {
    return (
      <div className="flex h-full items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 text-gray-500">
        로딩 중...
      </div>
    );
  }

  return (
    <div className="flex h-full bg-gradient-to-br from-violet-50 to-sky-50">
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
          onSessionChange={(id, lastCardUrl) => {
            handleSessionChange(id, lastCardUrl);
            setSidebarOpen(false);
          }}
          onLogout={handleLogout}
          refreshToken={sessionRefreshToken}
        />
      </div>

      {/* 모바일 사이드바 오버레이 배경 */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* 메인 영역 */}
      <div className="relative flex-1 overflow-hidden">
        {/* 모바일 사이드바 토글 버튼 */}
        <button
          className="md:hidden absolute top-3 left-3 z-10 rounded-full bg-white/90 px-3 py-1.5 text-xs text-gray-700 shadow-sm backdrop-blur-sm border border-gray-200"
          onClick={() => setSidebarOpen(true)}
        >
          ☰
        </button>

        {/* 슬라이딩 트랙: 모바일 200vw / 데스크탑 100% */}
        <div
          className={`flex h-full transition-transform duration-300 ease-in-out w-[200%] md:w-full ${
            activePane === "card"
              ? "-translate-x-1/2 md:translate-x-0"
              : "translate-x-0"
          }`}
          onTouchStart={onTouchStart}
          onTouchEnd={onTouchEnd}
        >
          {/* 채팅 영역: 모바일 50%(=100vw) / 데스크탑 40% */}
          <div className="w-1/2 md:w-2/5 h-full flex flex-col border-r border-gray-200 shadow-sm">
            <ChatPane
              childId={childId}
              sessionId={activeSessionId}
              onCardReady={handleCardReady}
              onLoadingChange={setIsLoading}
              currentBlock={currentBlock}
              onBlockChange={setCurrentBlock}
            />
          </div>

          {/* 카드 프리뷰 영역: 모바일 50%(=100vw) / 데스크탑 flex-1 */}
          <div className="relative w-1/2 md:flex-1 h-full">
            <CardPreview cardUrl={cardUrl} cardJson={cardJson} isLoading={isLoading} />

            {/* 좌측 에지 스와이프 캡처 존 */}
            <div
              className="md:hidden absolute inset-y-0 left-0 w-10 z-20"
              onTouchStart={onTouchStart}
              onTouchEnd={onTouchEnd}
            />

            {/* 채팅 복귀 버튼 */}
            <button
              className="md:hidden absolute top-3 left-3 z-20 rounded-full bg-white/90 px-3 py-1.5 text-xs text-gray-700 shadow-sm backdrop-blur-sm border border-gray-200"
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
              activePane === "chat" ? "bg-violet-500" : "bg-gray-300"
            }`}
          />
          <div
            className={`w-2 h-2 rounded-full transition-colors duration-200 ${
              activePane === "card" ? "bg-violet-500" : "bg-gray-300"
            }`}
          />
        </div>
      </div>
    </div>
  );
}
