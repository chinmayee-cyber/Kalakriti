"use client"

import { useEffect, useState } from "react"
import { Palette } from "lucide-react"
import { useRouter } from "next/navigation"

export default function HomePage() {
  const [showLogo, setShowLogo] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowLogo(false)
      router.push("/dashboard")
    }, 2000)

    return () => clearTimeout(timer)
  }, [router])

  if (showLogo) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-muted/20 to-background">
        <div className="logo-animation">
          <div className="inline-flex items-center gap-4 bg-primary text-primary-foreground px-8 py-6 rounded-3xl shadow-2xl">
            <Palette className="h-12 w-12" />
            <span className="text-4xl font-bold">Kalakriti</span>
          </div>
        </div>
      </div>
    )
  }

  return null
}
