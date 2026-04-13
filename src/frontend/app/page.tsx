"use client";

import { Suspense, useCallback, useState } from "react";
import { useSearchParams } from "next/navigation";
import ChatPane from "@/components/ChatPane";
import GamePreview from "@/components/GamePreview";
import { useSwipe } from "@/hooks/useSwipe";

function GameApp() {
  const searchParams = useSearchParams();
  const childId = searchParams.get("child") ?? "guest";

  const [gameHtml, setGameHtml] = useState("");
  const [currentBlock, setCurrentBlock] = useState(0);
  const [activePane, setActivePane] = useState<"chat" | "game">("chat");

  const handleGameHtmlChange = useCallback((html: string) => {
    setGameHtml(html);
  }, []);

  const { onTouchStart, onTouchEnd } = useSwipe({
    onSwipeLeft: () => setActivePane("game"),
    onSwipeRight: () => setActivePane("chat"),
  });

  return (
    <div className="relative h-full overflow-hidden bg-gray-950">
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
            onGameHtmlChange={handleGameHtmlChange}
            currentBlock={currentBlock}
            onBlockChange={setCurrentBlock}
          />
        </div>

        {/* 게임 프리뷰 영역: 모바일 50%(=100vw) / 데스크탑 flex-1 */}
        <div className="w-1/2 md:flex-1 h-full">
          <GamePreview html={gameHtml} />
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
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div className="flex h-full items-center justify-center bg-gray-950 text-gray-400">로딩 중...</div>}>
      <GameApp />
    </Suspense>
  );
}
