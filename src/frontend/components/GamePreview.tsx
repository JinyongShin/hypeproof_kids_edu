"use client";

import { useEffect, useState } from "react";

interface CardData {
  card_type: "character" | "world" | "title";
  name: string;
  description: string;
  traits: string[];
  world: string;
  image_prompt: string;
  effects?: string[];
}

interface CardPreviewProps {
  cardUrl: string;
  cardJson?: string;
  isLoading?: boolean;
}

function parseCardJson(jsonStr: string): CardData | null {
  try {
    return JSON.parse(jsonStr) as CardData;
  } catch {
    return null;
  }
}

function CardTypeLabel({ type }: { type: CardData["card_type"] }) {
  const labels = {
    character: { text: "캐릭터", bg: "bg-violet-100", color: "text-violet-700" },
    world: { text: "세계", bg: "bg-sky-100", color: "text-sky-700" },
    title: { text: "타이틀", bg: "bg-amber-100", color: "text-amber-700" },
  };
  const { text, bg, color } = labels[type] || labels.character;
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${bg} ${color}`}>
      {text}
    </span>
  );
}

export default function CardPreview({ cardUrl, cardJson, isLoading = false }: CardPreviewProps) {
  const card = cardJson ? parseCardJson(cardJson) : null;
  const [imageUrl, setImageUrl] = useState<string>("");
  const [imageLoading, setImageLoading] = useState(false);

  // image_prompt 있으면 프론트엔드에서 이미지 API 호출
  useEffect(() => {
    if (card?.image_prompt && !imageUrl) {
      setImageLoading(true);
      fetch(`${process.env.NEXT_PUBLIC_BACKEND_HTTP_URL ?? "http://localhost:8000"}/generate-image`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_prompt: card.image_prompt }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.image_base64) {
            setImageUrl(`data:${data.mime_type};base64,${data.image_base64}`);
          }
        })
        .catch(() => {})
        .finally(() => setImageLoading(false));
    }
  }, [card?.image_prompt]);

  if (!cardUrl && !cardJson) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-4 bg-gradient-to-br from-violet-50 to-sky-50 text-gray-500">
        {isLoading ? (
          <>
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
            <p className="text-lg text-gray-600">카드 만드는 중...</p>
          </>
        ) : (
          <>
            <div className="text-6xl">🎴</div>
            <p className="text-lg text-gray-700">AI에게 만들고 싶은 캐릭터를 말해봐!</p>
            <p className="text-sm text-gray-500">예: "토끼처럼 생긴 캐릭터 만들어줘"</p>
          </>
        )}
      </div>
    );
  }

  // 카드 데이터가 있으면 카드 UI 렌더링
  if (card) {
    return (
      <div className="relative h-full w-full flex items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 p-6">
        {/* 카드 컨테이너 */}
        <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
          {/* 카드 헤더 - 이미지 또는 이모지 */}
          <div className="bg-gradient-to-r from-violet-400 to-sky-400 px-6 py-8 text-center relative">
            {imageLoading ? (
              <div className="flex flex-col items-center gap-2">
                <div className="h-10 w-10 animate-spin rounded-full border-4 border-white/30 border-t-white" />
                <p className="text-sm text-white/70">이미지 만드는 중...</p>
              </div>
            ) : imageUrl ? (
              <img src={imageUrl} alt={card.name} className="w-full h-40 object-contain rounded-xl" />
            ) : (
              <div className="text-6xl mb-2">
                {card.card_type === "character" ? "🦸" : card.card_type === "world" ? "🌍" : "✨"}
              </div>
            )}
            <h2 className="text-2xl font-bold text-white drop-shadow-sm mt-2">{card.name}</h2>
          </div>

          {/* 카드 바디 */}
          <div className="px-6 py-5 space-y-4">
            {/* 카드 타입 */}
            <div className="flex justify-center">
              <CardTypeLabel type={card.card_type} />
            </div>

            {/* 설명 */}
            <p className="text-gray-700 text-center leading-relaxed">{card.description}</p>

            {/* 특성 태그 */}
            {card.traits && card.traits.length > 0 && (
              <div className="flex flex-wrap justify-center gap-2">
                {card.traits.map((trait, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-violet-50 text-violet-600 rounded-full text-sm font-medium"
                  >
                    {trait}
                  </span>
                ))}
              </div>
            )}

            {/* 세계 설명 */}
            {card.world && (
              <div className="bg-sky-50 rounded-2xl px-4 py-3 text-center">
                <p className="text-sm text-gray-500 mb-1">🌍 세계</p>
                <p className="text-sky-700">{card.world}</p>
              </div>
            )}

            {/* 꾸미기 효과 */}
            {card.effects && card.effects.length > 0 && (
              <div className="flex flex-wrap justify-center gap-2">
                {card.effects.map((effect, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-amber-50 text-amber-600 rounded-full text-sm"
                  >
                    ✨ {effect}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* 새 카드 생성 중 오버레이 */}
        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-white/70 backdrop-blur-sm">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
            <p className="text-sm text-gray-600">새 카드 만드는 중...</p>
          </div>
        )}
      </div>
    );
  }

  // JSON 파싱 실패 시 빈 카드 표시
  return (
    <div className="flex h-full flex-col items-center justify-center gap-4 bg-gradient-to-br from-violet-50 to-sky-50 text-gray-500">
      <div className="text-6xl">🎴</div>
      <p className="text-lg text-gray-700">카드를 불러오는 중...</p>
      {isLoading && (
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
      )}
    </div>
  );
}
