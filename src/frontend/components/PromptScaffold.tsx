"use client";

import { getScaffold } from "@/lib/scaffoldData";

interface PromptScaffoldProps {
  currentBlock: number;
  onSelect: (prompt: string) => void;
}

export default function PromptScaffold({ currentBlock, onSelect }: PromptScaffoldProps) {
  const scaffold = getScaffold(currentBlock);

  if (!scaffold || scaffold.prompts.length === 0) return null;

  return (
    <div className="border-b border-gray-200 bg-violet-50/50 px-4 py-2">
      <p className="mb-1 text-xs text-gray-600">
        <span className="font-medium text-violet-600">{scaffold.skill}</span>
        {" — "}
        {scaffold.skillDesc}
      </p>
      <div className="flex flex-wrap gap-1">
        {scaffold.prompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => onSelect(prompt)}
            className="rounded-full border border-violet-200 bg-white px-3 py-1 text-xs text-violet-700 transition-colors hover:bg-violet-100 hover:border-violet-300 shadow-sm"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
