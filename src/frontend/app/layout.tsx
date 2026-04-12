import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HypeProof Kids Edu",
  description: "AI와 함께 게임을 만들어요",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="h-full">
      <body className="h-full">{children}</body>
    </html>
  );
}
