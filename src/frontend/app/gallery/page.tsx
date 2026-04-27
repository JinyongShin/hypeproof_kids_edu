"use client"
import { BACKEND_HTTP_URL } from "@/lib/backendUrl";

import { useEffect, useState } from "react";

interface SavedGame {
  game_id: string;
  url: string;
  session_id: string;
  child_id: string;
  session_name: string;
  created_at: string;
}

export default function GalleryPage() {
  const [games, setGames] = useState<SavedGame[]>([]);
  const [current, setCurrent] = useState(0);
  const [autoPlay, setAutoPlay] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND_HTTP_URL}/gallery`)
      .then((r) => r.json())
      .then((data) => {
        setGames(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!autoPlay || games.length <= 1) return;
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % games.length);
    }, 12_000); // 게임 재생 시간 — 카드보다 길게
    return () => clearInterval(timer);
  }, [autoPlay, games.length]);

  const prev = () => {
    setCurrent((c) => (c - 1 + games.length) % games.length);
    setAutoPlay(false);
  };
  const next = () => {
    setCurrent((c) => (c + 1) % games.length);
    setAutoPlay(false);
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50">
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
      </div>
    );
  }

  if (games.length === 0) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-gradient-to-br from-violet-50 to-sky-50">
        <p className="text-2xl text-gray-600">아직 저장된 게임이 없어요 🎮</p>
        <p className="text-sm text-gray-500">
          마스터 개발자 단계에서 💾 저장 버튼을 눌러야 여기에 나타나요!
        </p>
      </div>
    );
  }

  const game = games[current];

  return (
    <div className="flex h-screen flex-col items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 p-4 md:p-6">
      {/* 진행 표시 */}
      <div className="mb-3 flex items-center gap-3 text-sm text-gray-500">
        <span>
          {current + 1} / {games.length}
        </span>
        <button
          onClick={() => setAutoPlay(!autoPlay)}
          className="rounded-full px-3 py-1 text-xs bg-violet-100 text-violet-600 hover:bg-violet-200"
        >
          {autoPlay ? "⏸ 자동" : "▶ 자동"}
        </button>
        <span className="text-xs text-gray-400 hidden md:inline">
          개발자: {game.child_id} · {game.session_name || "세션"}
        </span>
      </div>

      {/* 게임 iframe (런칭쇼 메인) */}
      <div className="w-full max-w-3xl flex-1 max-h-[70vh] bg-gray-900 rounded-2xl shadow-2xl overflow-hidden border-4 border-white">
        <iframe
          key={game.game_id}
          src={game.url}
          className="w-full h-full border-0"
          sandbox="allow-scripts"
          title={`Game ${game.game_id}`}
        />
      </div>

      {/* 게임 정보 */}
      <div className="mt-3 text-center">
        <p className="text-lg font-semibold text-gray-700">
          🎮 {game.session_name || `게임 ${current + 1}`}
        </p>
        <p className="text-xs text-gray-400 md:hidden">개발자: {game.child_id}</p>
      </div>

      {/* 네비게이션 */}
      <div className="mt-4 flex gap-3">
        <button
          onClick={prev}
          className="rounded-full bg-white px-5 py-2 text-base shadow-md hover:shadow-lg transition-shadow"
        >
          ◀ 이전
        </button>
        <button
          onClick={next}
          className="rounded-full bg-white px-5 py-2 text-base shadow-md hover:shadow-lg transition-shadow"
        >
          다음 ▶
        </button>
      </div>

      {/* 도트 인디케이터 */}
      <div className="mt-3 flex gap-1.5 max-w-full overflow-x-auto px-2">
        {games.map((_, i) => (
          <button
            key={i}
            onClick={() => {
              setCurrent(i);
              setAutoPlay(false);
            }}
            className={`h-2 rounded-full transition-all flex-shrink-0 ${
              i === current ? "w-6 bg-violet-500" : "w-2 bg-gray-300"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
