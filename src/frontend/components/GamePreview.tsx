"use client";

interface GamePreviewProps {
  /** 저장된 게임의 URL. 빈 문자열이면 대기 화면 표시. */
  gameUrl: string;
  /** 새 게임 생성 중 여부 */
  isLoading?: boolean;
}

export default function GamePreview({ gameUrl, isLoading = false }: GamePreviewProps) {
  if (!gameUrl) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-4 bg-gray-950 text-gray-500">
        {isLoading ? (
          <>
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-700 border-t-indigo-500" />
            <p className="text-lg text-gray-400">게임 만드는 중...</p>
          </>
        ) : (
          <>
            <div className="text-6xl">🎮</div>
            <p className="text-lg">AI에게 만들고 싶은 게임을 말해봐!</p>
            <p className="text-sm text-gray-600">예: "별을 모으는 게임 만들어줘"</p>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="relative h-full w-full">
      <iframe
        src={gameUrl}
        // allow-scripts: JS 실행 허용
        // allow-same-origin 금지: 부모 페이지 DOM 접근 차단
        sandbox="allow-scripts"
        className="h-full w-full border-0 bg-gray-950"
        title="게임 프리뷰"
      />
      {/* 새 게임 생성 중 오버레이 */}
      {isLoading && (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-gray-950/70 backdrop-blur-sm">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-700 border-t-indigo-500" />
          <p className="text-sm text-gray-300">새 게임 만드는 중...</p>
        </div>
      )}
    </div>
  );
}
