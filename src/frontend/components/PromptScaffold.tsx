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
    <div className="border-b border-gray-800 px-4 py-2">
      <p className="mb-1 text-xs text-gray-500">
        <span className="font-medium text-indigo-400">{scaffold.skill}</span>
        {" — "}
        {scaffold.skillDesc}
      </p>
      <div className="flex flex-wrap gap-1">
        {scaffold.prompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => onSelect(prompt)}
            className="rounded-full border border-indigo-800 bg-indigo-950 px-3 py-1 text-xs text-indigo-300 transition-colors hover:bg-indigo-900 hover:text-white"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
