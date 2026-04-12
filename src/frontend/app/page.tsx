"use client";

import { useState } from "react";
import GamePreview from "@/components/GamePreview";

export default function Home() {
  const [gameHtml, setGameHtml] = useState("");

  return (
    <div className="flex h-full bg-gray-950">
      {/* 채팅 영역 (40%) — Unit 5에서 ChatPane으로 교체 */}
      <div className="flex w-2/5 flex-col border-r border-gray-800 p-4 text-gray-400">
        <p className="text-sm">채팅 영역 (준비 중)</p>
        {/* 임시 테스트 버튼 */}
        <button
          className="mt-4 rounded bg-indigo-600 px-3 py-2 text-sm text-white hover:bg-indigo-500"
          onClick={() =>
            setGameHtml(
              `<!DOCTYPE html><html><body style="margin:0;background:#1a1a2e">
              <canvas id="c" width="400" height="400"></canvas>
              <script>
                const c=document.getElementById('c'),ctx=c.getContext('2d');
                ctx.fillStyle='#FFD700';ctx.font='48px sans-serif';
                ctx.fillText('⭐',180,220);
                ctx.fillStyle='#fff';ctx.font='20px sans-serif';
                ctx.fillText('게임 프리뷰 작동!',100,300);
              </script>
              </body></html>`,
            )
          }
        >
          테스트 게임 로드
        </button>
      </div>

      {/* 게임 프리뷰 영역 (60%) */}
      <div className="flex-1">
        <GamePreview html={gameHtml} />
      </div>
    </div>
  );
}
