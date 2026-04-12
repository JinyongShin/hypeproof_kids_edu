"use client";

import { Suspense, useCallback, useState } from "react";
import { useSearchParams } from "next/navigation";
import ChatPane from "@/components/ChatPane";
import GamePreview from "@/components/GamePreview";

function GameApp() {
  const searchParams = useSearchParams();
  const childId = searchParams.get("child") ?? "guest";

  const [gameHtml, setGameHtml] = useState("");
  const [currentBlock, setCurrentBlock] = useState(0);

  const handleGameHtmlChange = useCallback((html: string) => {
    setGameHtml(html);
  }, []);

  return (
    <div className="flex h-full bg-gray-950">
      {/* 채팅 영역 (40%) */}
      <div className="flex w-2/5 flex-col border-r border-gray-800 text-gray-100">
        <ChatPane
          childId={childId}
          onGameHtmlChange={handleGameHtmlChange}
          currentBlock={currentBlock}
          onBlockChange={setCurrentBlock}
        />
      </div>

      {/* 게임 프리뷰 영역 (60%) */}
      <div className="flex-1">
        <GamePreview html={gameHtml} />
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
