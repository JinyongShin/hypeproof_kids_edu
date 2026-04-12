"use client";

interface GamePreviewProps {
  /** Claude가 생성한 게임 HTML. 빈 문자열이면 대기 화면 표시. */
  html: string;
}

export default function GamePreview({ html }: GamePreviewProps) {
  if (!html) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-4 bg-gray-950 text-gray-500">
        <div className="text-6xl">🎮</div>
        <p className="text-lg">AI에게 만들고 싶은 게임을 말해봐!</p>
        <p className="text-sm text-gray-600">예: "별을 모으는 게임 만들어줘"</p>
      </div>
    );
  }

  return (
    <iframe
      // srcdoc으로 HTML 직접 주입 — 외부 URL 없이 실행
      srcDoc={html}
      // allow-scripts: JS 실행 허용
      // allow-same-origin 금지: 부모 페이지 DOM 접근 차단
      sandbox="allow-scripts"
      className="h-full w-full border-0 bg-gray-950"
      title="게임 프리뷰"
    />
  );
}
