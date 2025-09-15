"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  TrendingUp,
  GraduationCap,
  Instagram,
  DollarSign,
  Package,
  ShoppingCart,
  Eye,
  Users,
  Home,
  Palette,
  Heart,
  Play,
  ChevronLeft,
  ChevronRight,
} from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

const sidebarItems = [
  { icon: Home, label: "Overview", href: "/dashboard", active: true },
  { icon: TrendingUp, label: "Market Trends", href: "/dashboard/market-trends" },
  { icon: Instagram, label: "Social Promotion", href: "/dashboard/social-promotion" },
  { icon: GraduationCap, label: "Art Education", href: "/dashboard/art-education" },
  { icon: DollarSign, label: "Crypto Valuation", href: "/dashboard/crypto-valuation" },
  { icon: Package, label: "Supply Chain", href: "/dashboard/supply-chain" },
  { icon: ShoppingCart, label: "Art Auction", href: "/dashboard/art-auction" },
  { icon: Eye, label: "Multimodal Experience", href: "/dashboard/multimodal-experience" },
  { icon: Users, label: "Inclusive Promotion", href: "/dashboard/inclusive-promotion" },
]

const featuredArtworks = [
  {
    id: 1,
    title: "Madhubani Harmony",
    artist: "Priya Sharma",
    image: "/madhubani-painting-colorful-traditional.jpg",
    likes: 1247,
    views: 8934,
    liked: false,
  },
  {
    id: 2,
    title: "Tanjore Elegance",
    artist: "Rajesh Kumar",
    image: "/tanjore-painting-gold-traditional.jpg",
    likes: 892,
    views: 5621,
    liked: true,
  },
  {
    id: 3,
    title: "Warli Village Life",
    artist: "Meera Patel",
    image: "/placeholder-tiv7h.png",
    likes: 1456,
    views: 9876,
    liked: false,
  },
]

const topAuctions = [
  { title: "Royal Miniature", currentBid: "₹45,000", timeLeft: "2h 15m" },
  { title: "Kalamkari Masterpiece", currentBid: "₹32,000", timeLeft: "5h 42m" },
  { title: "Pattachitra Story", currentBid: "₹28,500", timeLeft: "1d 3h" },
]

export default function DashboardPage() {
  const [sidebarExpanded, setSidebarExpanded] = useState(false)
  const [currentSlide, setCurrentSlide] = useState(0)
  const [artworkLikes, setArtworkLikes] = useState(
    featuredArtworks.reduce((acc, artwork) => ({ ...acc, [artwork.id]: artwork.liked }), {}),
  )

  const toggleLike = (artworkId: number) => {
    setArtworkLikes((prev) => ({ ...prev, [artworkId]: !prev[artworkId] }))
  }

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % featuredArtworks.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + featuredArtworks.length) % featuredArtworks.length)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-muted/20 to-background">
      <div
        className={cn(
          "fixed left-0 top-0 z-50 h-full bg-card border-r border-border transition-all duration-300 ease-in-out",
          sidebarExpanded ? "w-64" : "w-16",
        )}
        onMouseEnter={() => setSidebarExpanded(true)}
        onMouseLeave={() => setSidebarExpanded(false)}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="bg-primary text-primary-foreground p-2 rounded-lg">
              <Palette className="h-6 w-6" />
            </div>
            {sidebarExpanded && (
              <div className="overflow-hidden">
                <h2 className="font-bold text-lg text-primary">Kalakriti</h2>
                <p className="text-xs text-muted-foreground">Artist Dashboard</p>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar Navigation */}
        <nav className="p-2 space-y-2">
          {sidebarItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <div
                className={cn(
                  "flex items-center gap-3 p-3 rounded-lg transition-colors hover:bg-muted group",
                  item.active && "bg-primary/10 text-primary",
                )}
              >
                <item.icon className="h-5 w-5 shrink-0" />
                {sidebarExpanded && <span className="font-medium overflow-hidden whitespace-nowrap">{item.label}</span>}
              </div>
            </Link>
          ))}
        </nav>

        {/* Sidebar Footer */}
        {sidebarExpanded && (
          <div className="absolute bottom-4 left-4 right-4">
            <Card className="bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/20">
              <CardContent className="p-4">
                <p className="text-sm font-medium">Need Help?</p>
                <p className="text-xs text-muted-foreground mb-2">Get support from our team</p>
                <Button size="sm" variant="outline" className="w-full bg-transparent">
                  Contact Support
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className={cn("transition-all duration-300", sidebarExpanded ? "ml-64" : "ml-16")}>
        {/* Header */}
        <header className="bg-card/80 backdrop-blur-sm border-b border-border sticky top-0 z-40">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gradient">Dashboard Overview</h1>
                <p className="text-muted-foreground">Manage your artistic journey with AI-powered tools</p>
              </div>
              <div className="flex items-center gap-4">
                <Badge variant="secondary" className="bg-secondary/20 text-secondary-foreground">
                  Active Artist
                </Badge>
                <Link href="/">
                  <Button variant="outline" size="sm">
                    Back to Home
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="p-6">
          {/* Welcome Section */}
          <div className="mb-8">
            <Card className="bg-gradient-to-r from-primary/5 via-secondary/5 to-accent/5 border-primary/20">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-semibold mb-2">Welcome back, Artist!</h2>
                    <p className="text-muted-foreground">
                      Explore our AI-powered tools to enhance your artistic journey and reach global audiences.
                    </p>
                  </div>
                  <div className="hidden md:block">
                    <div className="bg-primary/10 p-4 rounded-full">
                      <Palette className="h-8 w-8 text-primary" />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="mb-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  Featured Artworks
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={prevSlide}>
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm" onClick={nextSlide}>
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </CardTitle>
                <CardDescription>Most liked and viewed artworks from our community</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="relative overflow-hidden rounded-lg">
                  <div
                    className="flex transition-transform duration-300 ease-in-out"
                    style={{ transform: `translateX(-${currentSlide * 100}%)` }}
                  >
                    {featuredArtworks.map((artwork) => (
                      <div key={artwork.id} className="w-full flex-shrink-0">
                        <div className="relative">
                          <img
                            src={artwork.image || "/placeholder.svg"}
                            alt={artwork.title}
                            className="w-full h-64 object-cover rounded-lg"
                          />
                          <div className="absolute bottom-0 left-0 right-0 bg-black/85 p-4 rounded-b-lg">
                            <h3 className="text-white font-semibold text-lg">{artwork.title}</h3>
                            <p className="text-white/95 text-sm">by {artwork.artist}</p>
                            <div className="flex items-center justify-between mt-2">
                              <div className="flex items-center gap-4 text-white/95 text-sm">
                                <span>{artwork.views.toLocaleString()} views</span>
                                <span>{artwork.likes.toLocaleString()} likes</span>
                              </div>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => toggleLike(artwork.id)}
                                className="text-white hover:bg-white/20"
                              >
                                <Heart
                                  className={cn("h-4 w-4", artworkLikes[artwork.id] ? "fill-red-500 text-red-500" : "")}
                                />
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Art Auction Marketplace */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <ShoppingCart className="h-5 w-5 text-primary" />
                  Top Auction Bids
                </CardTitle>
                <CardDescription>Live auctions with highest current bids</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topAuctions.map((auction, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div>
                        <p className="font-medium">{auction.title}</p>
                        <p className="text-sm text-muted-foreground">Ends in {auction.timeLeft}</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-primary">{auction.currentBid}</p>
                        <Button size="sm" variant="outline" className="mt-1 bg-transparent">
                          Bid Now
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
                <Link href="/dashboard/art-auction">
                  <Button className="w-full mt-4">View All Auctions</Button>
                </Link>
              </CardContent>
            </Card>

            {/* Art Education Video */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <GraduationCap className="h-5 w-5 text-secondary" />
                  Featured Course
                </CardTitle>
                <CardDescription>Learn traditional Madhubani painting techniques</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="relative bg-muted rounded-lg overflow-hidden">
                  <div className="aspect-video flex items-center justify-center bg-gradient-to-br from-secondary/20 to-accent/20">
                    <div className="text-center">
                      <div className="bg-secondary/20 p-4 rounded-full mb-4 inline-block">
                        <Play className="h-8 w-8 text-secondary" />
                      </div>
                      <h3 className="font-semibold mb-2">Madhubani Art Basics</h3>
                      <p className="text-sm text-muted-foreground mb-4">Duration: 45 minutes</p>
                      <Button className="bg-secondary hover:bg-secondary/90">Start Learning</Button>
                    </div>
                  </div>
                </div>
                <Link href="/dashboard/art-education">
                  <Button variant="outline" className="w-full mt-4 bg-transparent">
                    Browse All Courses
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}
