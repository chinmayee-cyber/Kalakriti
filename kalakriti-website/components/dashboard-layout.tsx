"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import {
  Home,
  TrendingUp,
  GraduationCap,
  Instagram,
  Coins,
  Package,
  ShoppingCart,
  Eye,
  Users,
  Palette,
  ArrowLeft,
} from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

const sidebarItems = [
  { icon: Home, label: "Overview", href: "/dashboard" },
  { icon: TrendingUp, label: "Market Trends", href: "/dashboard/market-trends" },
  { icon: GraduationCap, label: "Art Education", href: "/dashboard/art-education" },
  { icon: Instagram, label: "Social Promotion", href: "/dashboard/social-promotion" },
  { icon: Coins, label: "Crypto Valuation", href: "/dashboard/crypto-valuation" },
  { icon: Package, label: "Supply Chain", href: "/dashboard/supply-chain" },
  { icon: ShoppingCart, label: "Art Auction", href: "/dashboard/art-auction" },
  { icon: Eye, label: "Multimodal Experience", href: "/dashboard/multimodal-experience" },
  { icon: Users, label: "Inclusive Promotion", href: "/dashboard/inclusive-promotion" },
]

interface DashboardLayoutProps {
  children: React.ReactNode
  title: string
  description: string
  backHref?: string
}

export function DashboardLayout({ children, title, description, backHref = "/dashboard" }: DashboardLayoutProps) {
  const [sidebarExpanded, setSidebarExpanded] = useState(false)

  return (
    <div className="min-h-screen">
      <div
        className={cn(
          "fixed left-0 top-0 z-50 h-full bg-gradient-to-b from-card via-card/95 to-card border-r border-border/50 backdrop-blur-sm transition-all duration-300 ease-in-out shadow-lg",
          sidebarExpanded ? "w-64" : "w-16",
        )}
        onMouseEnter={() => setSidebarExpanded(true)}
        onMouseLeave={() => setSidebarExpanded(false)}
      >
        <div className="p-4 border-b border-border/50 bg-gradient-to-r from-primary/10 via-secondary/10 to-accent/10">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-primary to-secondary text-primary-foreground p-2 rounded-lg shadow-md">
              <Palette className="h-6 w-6" />
            </div>
            {sidebarExpanded && (
              <div className="overflow-hidden">
                <h2 className="font-bold text-lg text-gradient">Kalakriti</h2>
                <p className="text-xs text-muted-foreground">Artist Dashboard</p>
              </div>
            )}
          </div>
        </div>

        <nav className="p-2 space-y-1">
          {sidebarItems.map((item, index) => {
            const colorClasses = [
              "hover:bg-gradient-to-r hover:from-primary/10 hover:to-primary/5 hover:border-primary/20",
              "hover:bg-gradient-to-r hover:from-secondary/10 hover:to-secondary/5 hover:border-secondary/20",
              "hover:bg-gradient-to-r hover:from-accent/10 hover:to-accent/5 hover:border-accent/20",
            ]
            return (
              <Link key={item.href} href={item.href}>
                <div
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg transition-all duration-200 border border-transparent group",
                    colorClasses[index % 3],
                  )}
                >
                  <item.icon className="h-5 w-5 shrink-0 group-hover:scale-110 transition-transform" />
                  {sidebarExpanded && (
                    <span className="font-medium overflow-hidden whitespace-nowrap text-sm">{item.label}</span>
                  )}
                </div>
              </Link>
            )
          })}
        </nav>

        {sidebarExpanded && (
          <div className="absolute bottom-4 left-4 right-4">
            <Card className="bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10 border-primary/20 shadow-md">
              <CardContent className="p-4">
                <p className="text-sm font-medium text-gradient">Need Help?</p>
                <p className="text-xs text-muted-foreground mb-2">Get support from our team</p>
                <Button
                  size="sm"
                  variant="outline"
                  className="w-full bg-gradient-to-r from-primary/5 to-secondary/5 hover:from-primary/10 hover:to-secondary/10 border-primary/20"
                >
                  Contact Support
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className={cn("transition-all duration-300", sidebarExpanded ? "ml-64" : "ml-16")}>
        <header className="bg-gradient-to-r from-card/90 via-card/95 to-card/90 backdrop-blur-sm border-b border-border/50 sticky top-0 z-40 shadow-sm">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <Link href={backHref}>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-2 hover:bg-gradient-to-r hover:from-primary/10 hover:to-secondary/10"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    Back
                  </Button>
                </Link>
                <div>
                  <h1 className="text-2xl font-bold text-gradient">{title}</h1>
                  <p className="text-muted-foreground">{description}</p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6">{children}</main>
      </div>
    </div>
  )
}
