import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'IA Sarcastique - Détecteur de Questions Bêtes',
  description: 'Une IA qui détecte les questions stupides et répond avec sarcasme',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  )
}
