"use client"
import { BACKEND_HTTP_URL } from "@/lib/backendUrl";
import { useEffect, useState } from "react";


interface CardData {
  card_type: "character" | "world" | "title";
  name: string;
  description: string;
  traits: string[];
  world: string;
  image_prompt: string;
  image_svg?: string;
  effects?: string[];
}

// LLM이 만든 SVG는 우리 출력이지만 인라인 렌더 전 sanitize. <svg>로 시작 안 하면 거부.
function sanitizeSvg(raw: string | undefined | null): string {
  if (!raw || typeof raw !== "string") return "";
  const trimmed = raw.trim();
  if (!trimmed.toLowerCase().startsWith("<svg")) return "";
  if (trimmed.length > 4000) return "";
  return trimmed
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<foreignObject[\s\S]*?<\/foreignObject>/gi, "")
    .replace(/\son\w+\s*=\s*("[^"]*"|'[^']*')/gi, "")
    .replace(/(href|xlink:href)\s*=\s*("javascript:[^"]*"|'javascript:[^']*')/gi, "")
    .replace(/(href|xlink:href)\s*=\s*("https?:[^"]*"|'https?:[^']*')/gi, "");
}

interface CardPreviewProps {
  cardUrl: string;
  cardJson?: string;
  isLoading?: boolean;
  gameHtml?: string;
  sessionId?: string;
  childId?: string;
  gameUrl?: string;
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

// /games/{child}/{session}/{game_id}.html 또는 .../game_id 경로에서 id 추출
function extractGameId(url: string): string {
  const match = url.match(/\/games\/[^/]+\/[^/]+\/([^/?]+?)(?:\.html)?(?:[?#].*)?$/);
  return match ? match[1] : "";
}

export default function CardPreview({
  cardUrl,
  cardJson,
  isLoading = false,
  gameHtml = "",
  sessionId = "",
  childId = "",
  gameUrl = "",
}: CardPreviewProps) {
  const card = cardJson ? parseCardJson(cardJson) : null;
  const safeSvg = card?.image_svg ? sanitizeSvg(card.image_svg) : "";

  // 세계 구축 합성 뷰: 최신 character + 최신 world를 세션 동안 보존
  const [latestCharacter, setLatestCharacter] = useState<CardData | null>(null);
  const [latestWorld, setLatestWorld] = useState<CardData | null>(null);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "saved" | "error">("idle");
  const [showGame, setShowGame] = useState(true);

  // 세션 전환 시 합성 슬롯과 저장 상태 리셋
  useEffect(() => {
    setLatestCharacter(null);
    setLatestWorld(null);
    setSaveStatus("idle");
    setShowGame(true);
  }, [sessionId]);

  // 새 게임 도착 시 자동으로 게임 뷰 표시
  useEffect(() => {
    if (gameHtml) setShowGame(true);
  }, [gameHtml]);

  // 새 카드 도착 → 타입별 슬롯 갱신
  useEffect(() => {
    if (!card) return;
    if (card.card_type === "character") setLatestCharacter(card);
    else if (card.card_type === "world") setLatestWorld(card);
  }, [card?.card_type, cardJson]);

  // 새 게임 생성 시 저장 상태 초기화 (덮어쓰기 가능)
  useEffect(() => {
    setSaveStatus("idle");
  }, [gameUrl, gameHtml]);

  const handleSave = async () => {
    if (!gameUrl || !childId || !sessionId) return;
    const gameId = extractGameId(gameUrl);
    if (!gameId) {
      setSaveStatus("error");
      return;
    }
    setSaveStatus("saving");
    try {
      const r = await fetch(
        `${BACKEND_HTTP_URL}/games/${childId}/${sessionId}/${gameId}/save`,
        { method: "POST" }
      );
      setSaveStatus(r.ok ? "saved" : "error");
    } catch {
      setSaveStatus("error");
    }
  };

  // 빈 상태
  if (!cardUrl && !cardJson && !gameHtml) {
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
            <p className="text-sm text-gray-500">예: &quot;토끼처럼 생긴 캐릭터 만들어줘&quot;</p>
          </>
        )}
      </div>
    );
  }

  // 게임 HTML — showGame=true면 게임 iframe, false면 카드 뷰로 fall-through
  if (gameHtml && showGame) {
    const canSave = Boolean(gameUrl && childId && sessionId);
    const saveLabel =
      saveStatus === "saved"
        ? "✅ 저장됨"
        : saveStatus === "saving"
        ? "💾 저장 중..."
        : saveStatus === "error"
        ? "❌ 다시"
        : "💾 저장";
    return (
      <div className="relative h-full w-full bg-gray-900">
        <iframe
          srcDoc={gameHtml}
          className="w-full h-full border-0"
          sandbox="allow-scripts"
          title="Game"
        />
        {canSave && (
          <button
            onClick={handleSave}
            disabled={saveStatus === "saving"}
            className={`absolute top-3 right-3 z-10 rounded-full px-4 py-2 text-sm font-semibold shadow-lg backdrop-blur-sm transition-colors ${
              saveStatus === "saved"
                ? "bg-emerald-500 text-white hover:bg-emerald-500"
                : saveStatus === "error"
                ? "bg-red-500 text-white hover:bg-red-600"
                : saveStatus === "saving"
                ? "bg-white/80 text-gray-500"
                : "bg-white/95 text-violet-700 hover:bg-white"
            }`}
            title="저장하면 갤러리(런칭쇼)에 등록돼. 다시 누르면 덮어쓰기 돼."
          >
            {saveLabel}
          </button>
        )}
        <button
          onClick={() => setShowGame(false)}
          className="absolute bottom-3 left-3 z-10 rounded-full bg-white/90 px-3 py-1.5 text-xs text-gray-700 shadow-sm backdrop-blur-sm border border-gray-200 hover:bg-white"
        >
          🎴 카드 보기
        </button>
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/70 backdrop-blur-sm">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
          </div>
        )}
      </div>
    );
  }

  // 합성 뷰 — 캐릭터 + 세계 둘 다 있을 때 (Block 2: 세계 구축)
  const hasComposite = latestCharacter && latestWorld;
  if (hasComposite) {
    const charSvg = sanitizeSvg(latestCharacter!.image_svg);
    const worldSvg = sanitizeSvg(latestWorld!.image_svg);
    return (
      <div className="relative h-full w-full flex items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 p-6">
        {gameHtml && (
          <button
            onClick={() => setShowGame(true)}
            className="absolute top-3 right-3 z-10 rounded-full bg-violet-500 px-3 py-1.5 text-xs text-white shadow-sm hover:bg-violet-600"
          >
            🎮 게임 보기
          </button>
        )}
        <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
          {/* 합성 캔버스 — 배경(world) + 캐릭터(중앙) */}
          <div className="bg-gradient-to-r from-violet-400 to-sky-400 px-6 py-8 text-center">
            <div className="relative mx-auto w-64 h-64 rounded-2xl overflow-hidden shadow-inner bg-white/95">
              {worldSvg ? (
                <div
                  className="absolute inset-0 [&_svg]:w-full [&_svg]:h-full [&_svg]:block"
                  dangerouslySetInnerHTML={{ __html: worldSvg }}
                />
              ) : (
                <div className="absolute inset-0 bg-gradient-to-b from-sky-200 to-violet-200" />
              )}
              {charSvg && (
                <div
                  className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-3/5 h-3/5 [&_svg]:w-full [&_svg]:h-full [&_svg]:block drop-shadow-[0_4px_8px_rgba(0,0,0,0.25)]"
                  dangerouslySetInnerHTML={{ __html: charSvg }}
                />
              )}
            </div>
            <h2 className="mt-4 text-2xl font-bold text-white drop-shadow-sm">
              {latestCharacter!.name}
            </h2>
            <p className="mt-1 text-sm text-white/85">
              {latestWorld!.name}에서 ✨
            </p>
          </div>

          {/* 바디 — 합성 정보 */}
          <div className="px-6 py-5 space-y-3">
            <div className="flex justify-center gap-2 flex-wrap">
              <span className="px-3 py-1 rounded-full text-xs bg-violet-100 text-violet-700 font-medium">
                🦸 {latestCharacter!.name}
              </span>
              <span className="px-3 py-1 rounded-full text-xs bg-sky-100 text-sky-700 font-medium">
                🌍 {latestWorld!.name}
              </span>
            </div>
            <p className="text-gray-700 text-center text-sm leading-relaxed">
              {latestWorld!.description}
            </p>
          </div>
        </div>

        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-white/70 backdrop-blur-sm">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
            <p className="text-sm text-gray-600">세계를 다듬는 중...</p>
          </div>
        )}
      </div>
    );
  }

  // 단일 카드 뷰 — 아바타 소환 단계 또는 세계만 있는 상태
  if (card) {
    return (
      <div className="relative h-full w-full flex items-center justify-center bg-gradient-to-br from-violet-50 to-sky-50 p-6">
        {gameHtml && (
          <button
            onClick={() => setShowGame(true)}
            className="absolute top-3 right-3 z-10 rounded-full bg-violet-500 px-3 py-1.5 text-xs text-white shadow-sm hover:bg-violet-600"
          >
            🎮 게임 보기
          </button>
        )}
        <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
          <div className="bg-gradient-to-r from-violet-400 to-sky-400 px-6 py-8 text-center relative">
            {safeSvg ? (
              <div
                className="mx-auto w-40 h-40 rounded-2xl bg-white/95 p-2 shadow-inner [&_svg]:w-full [&_svg]:h-full [&_svg]:block"
                dangerouslySetInnerHTML={{ __html: safeSvg }}
              />
            ) : (
              <div className="text-6xl mb-2">
                {card.card_type === "character" ? "🦸" : card.card_type === "world" ? "🌍" : "✨"}
              </div>
            )}
            <h2 className="text-2xl font-bold text-white drop-shadow-sm mt-2">{card.name}</h2>
          </div>

          <div className="px-6 py-5 space-y-4">
            <div className="flex justify-center">
              <CardTypeLabel type={card.card_type} />
            </div>

            <p className="text-gray-700 text-center leading-relaxed">{card.description}</p>

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

            {card.world && (
              <div className="bg-sky-50 rounded-2xl px-4 py-3 text-center">
                <p className="text-sm text-gray-500 mb-1">🌍 세계</p>
                <p className="text-sky-700">{card.world}</p>
              </div>
            )}

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

        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-white/70 backdrop-blur-sm">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-200 border-t-violet-500" />
            <p className="text-sm text-gray-600">새 카드 만드는 중...</p>
          </div>
        )}
      </div>
    );
  }

  // JSON 파싱 실패 폴백
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
