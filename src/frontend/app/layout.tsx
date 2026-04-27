import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HypeProof Kids Edu",
  description: "AI와 함께 타이틀 카드를 만들어요",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="h-full">
      <head>
        <script src="/_backend.js" />
      </head>
      <body className="h-full bg-gradient-to-br from-violet-50 to-sky-50">{children}</body>
    </html>
  );
}
