import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { TrademarkCopilot } from "@/components/TrademarkCopilot"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "DClaw Trademark",
  description: "Trademark management SaaS — search, file, monitor, and manage your trademark portfolio",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <TrademarkCopilot />
      </body>
    </html>
  )
}
