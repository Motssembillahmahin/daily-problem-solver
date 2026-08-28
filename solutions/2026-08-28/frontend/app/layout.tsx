import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: "Show HN: We built open OpenRouter that turns usage into a better model",
    description: "AI-powered solution",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}