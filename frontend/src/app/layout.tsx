import type { Metadata } from "next";
import { IBM_Plex_Sans_Arabic, Inter } from "next/font/google";
import "./globals.css";

const arabicFont = IBM_Plex_Sans_Arabic({
  subsets: ["arabic"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-arabic"
});

const latinFont = Inter({
  subsets: ["latin"],
  variable: "--font-latin"
});

export const metadata: Metadata = {
  title: "خفيفة | مروحة خصر وباور بانك",
  description:
    "متجر خفيفة الكويتي لمنتجات الراحة العملية. مروحة خصر مع باور بانك للدفع عند الاستلام داخل الكويت."
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ar-KW" dir="rtl">
      <body className={`${arabicFont.variable} ${latinFont.variable} font-sans`}>
        {children}
      </body>
    </html>
  );
}
