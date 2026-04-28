"use client"
import { BACKEND_HTTP_URL, BACKEND_WS_URL } from "@/lib/backendUrl";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";


export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (typeof window !== "undefined" && sessionStorage.getItem("child_id")) {
      router.replace("/");
    }
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const res = await fetch(`${BACKEND_HTTP_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (res.ok) {
        const { child_id } = await res.json();
        sessionStorage.setItem("child_id", child_id);
        router.push("/");
      } else {
        const body = await res.json().catch(() => ({}));
        setError(body.detail ?? "아이디 또는 비밀번호가 틀렸어요");
      }
    } catch {
      setError("서버에 연결할 수 없어요. 잠깐 기다렸다 다시 해봐!");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full items-center justify-center bg-gray-950">
      <form
        onSubmit={handleSubmit}
        className="flex w-80 flex-col gap-4 rounded-2xl bg-gray-900 p-8 shadow-lg"
      >
        <h1 className="text-center text-2xl font-bold text-white">
          🎮 Kids Edu
        </h1>
        <input
          type="text"
          placeholder="아이디"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
          required
          className="rounded-xl border border-gray-700 bg-gray-800 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-indigo-500"
        />
        <input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          required
          className="rounded-xl border border-gray-700 bg-gray-800 px-4 py-3 text-white placeholder-gray-500 outline-none focus:border-indigo-500"
        />
        {error && (
          <p className="text-center text-sm text-red-400">{error}</p>
        )}
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-xl bg-indigo-600 py-3 font-semibold text-white transition-colors hover:bg-indigo-500 disabled:opacity-50"
        >
          {isLoading ? "로그인 중..." : "시작하기"}
        </button>
      </form>
    </div>
  );
}
