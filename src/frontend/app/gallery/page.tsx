"use client";

import { useEffect, useState } from "react";

interface CardData {
  card_id: string;
  card_type: "character" | "world" | "title";
  name: string;
  description: string;
  traits: string[];
  world: string;
  image_prompt: string;
  child_name: string;
  created_at: string;
}

export default function GalleryPage() {
  const [cards, setCards] = useState<CardData[]>([]);
  const [current, setCurrent] = useState(0);
  const [autoPlay, setAutoPlay] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/gallery")
      .then((r) => r.json())
      .then((data) => {
        setCards(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!autoPlay || cards.length === 0) return;
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % cards.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [autoPlay, cards.length]);

  const prev = () => {
    setCurrent((c) => (c - 1 + cards.length) % cards.length);
    setAutoPlay(false);
  };
  const next = () => {
    setCurrent((c) => (c + 1) % cards.length);
    setAutoPlay(false);
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50">
        <div className="h-16 w-16 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
      </div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="flex h-screen items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50">
        <p className="text-2xl text-gray-500">아직 만들어진 카드가 없어요 🎴</p>
      </div>
    );
  }

  const card = cards[current];
  const typeEmoji = card.card_type === "character" ? "🦸" : card.card_type === "world" ? "🌍" : "✨";

  return (
    <div className="flex h-screen flex-col items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 p-8">
      {/* 진행 표시 */}
      <div className="mb-4 text-lg text-gray-400">
        {current + 1} / {cards.length}
        <button
          onClick={() => setAutoPlay(!autoPlay)}
          className="ml-4 rounded-full px-3 py-1 text-sm bg-violet-100 text-violet-600 hover:bg-violet-200"
        >
          {autoPlay ? "⏸ 자동" : "▶ 자동"}
        </button>
      </div>

      {/* 카드 */}
      <div className="w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-gray-100 overflow-hidden transition-all duration-500">
        <div className="bg-gradient-to-r from-violet-400 to-sky-400 px-8 py-10 text-center">
          <div className="text-7xl mb-3">{typeEmoji}</div>
          <h2 className="text-3xl font-bold text-white drop-shadow-sm">{card.name}</h2>
        </div>

        <div className="px-8 py-6 space-y-5">
          {/* 개발자 이름 */}
          <p className="text-center text-sm text-violet-500 font-medium">개발자: {card.child_name}</p>

          {/* 설명 */}
          <p className="text-gray-700 text-center text-lg leading-relaxed">{card.description}</p>

          {/* 특성 태그 */}
          {card.traits && card.traits.length > 0 && (
            <div className="flex flex-wrap justify-center gap-2">
              {card.traits.map((trait, i) => (
                <span key={i} className="px-4 py-1.5 bg-violet-50 text-violet-600 rounded-full text-sm font-medium">
                  {trait}
                </span>
              ))}
            </div>
          )}

          {/* 세계 설명 */}
          {card.world && (
            <div className="bg-sky-50 rounded-2xl px-5 py-4 text-center">
              <p className="text-sm text-gray-500 mb-1">🌍 세계</p>
              <p className="text-sky-700 text-lg">{card.world}</p>
            </div>
          )}
        </div>
      </div>

      {/* 네비게이션 */}
      <div className="mt-6 flex gap-4">
        <button
          onClick={prev}
          className="rounded-full bg-white px-6 py-3 text-lg shadow-md hover:shadow-lg transition-shadow"
        >
          ◀ 이전
        </button>
        <button
          onClick={next}
          className="rounded-full bg-white px-6 py-3 text-lg shadow-md hover:shadow-lg transition-shadow"
        >
          다음 ▶
        </button>
      </div>

      {/* 도트 인디케이터 */}
      <div className="mt-4 flex gap-1.5">
        {cards.map((_, i) => (
          <button
            key={i}
            onClick={() => { setCurrent(i); setAutoPlay(false); }}
            className={`h-2 rounded-full transition-all ${i === current ? "w-6 bg-violet-500" : "w-2 bg-gray-300"}`}
          />
        ))}
      </div>
    </div>
  );
}
