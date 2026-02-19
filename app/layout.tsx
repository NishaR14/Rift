import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PharmaGuard - AI-Powered Pharmacogenomic Risk Assessment',
  description: 'Analyze patient genetic data and predict personalized pharmacogenomic risks',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
