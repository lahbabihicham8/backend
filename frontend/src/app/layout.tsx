import type { Metadata } from "next";
import { PixelLoader } from "@/components/pixel-loader";
import "./globals.css";

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
      <body>
        {children}
        <PixelLoader />
      </body>
    </html>
  );
}
