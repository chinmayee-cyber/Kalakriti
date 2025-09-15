"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Gavel, TrendingUp, Eye, Heart, Users, Timer, DollarSign } from "lucide-react"

const liveAuctions = [
  {
    id: 1,
    title: "Contemporary Madhubani Art",
    artist: "Priya Sharma",
    currentBid: "₹25,000",
    startingBid: "₹15,000",
    timeLeft: "2h 45m",
    bidders: 12,
    image: "/placeholder.svg?key=auction1",
    category: "Traditional",
    views: 234,
  },
  {
    id: 2,
    title: "Digital Warli Fusion",
    artist: "Amit Patel",
    currentBid: "₹18,500",
    startingBid: "₹10,000",
    timeLeft: "5h 20m",
    bidders: 8,
    image: "/placeholder.svg?key=auction2",
    category: "Digital",
    views: 189,
  },
  {
    id: 3,
    title: "Tanjore Gold Leaf Painting",
    artist: "Meera Devi",
    currentBid: "₹45,000",
    startingBid: "₹30,000",
    timeLeft: "1h 15m",
    bidders: 18,
    image: "/placeholder.svg?key=auction3",
    category: "Classical",
    views: 456,
  },
]

const myAuctions = [
  {
    id: 1,
    title: "Village Life Madhubani",
    status: "Active",
    currentBid: "₹22,000",
    startingBid: "₹15,000",
    timeLeft: "3h 30m",
    bidders: 9,
    views: 167,
  },
  {
    id: 2,
    title: "Modern Warli Art",
    status: "Sold",
    finalBid: "₹35,000",
    startingBid: "₹20,000",
    soldDate: "Dec 10, 2024",
    bidders: 15,
    views: 289,
  },
]

const auctionStats = [
  {
    title: "Total Sales",
    value: "₹2,45,000",
    change: "+18%",
    icon: DollarSign,
    color: "text-green-600",
  },
  {
    title: "Active Auctions",
    value: "3",
    change: "+2",
    icon: Gavel,
    color: "text-blue-600",
  },
  {
    title: "Avg Sale Price",
    value: "₹28,500",
    change: "+12%",
    icon: TrendingUp,
    color: "text-purple-600",
  },
  {
    title: "Success Rate",
    value: "92%",
    change: "+5%",
    icon: Users,
    color: "text-orange-600",
  },
]

export default function ArtAuctionPage() {
  return (
    <DashboardLayout
      title="Art Auction Marketplace"
      description="Dynamic auction platform for buying and selling art with transparent pricing"
    >
      {/* Auction Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {auctionStats.map((stat, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <p className={`text-sm ${stat.color}`}>{stat.change} this month</p>
                </div>
                <div className="p-3 rounded-lg bg-muted">
                  <stat.icon className={`h-6 w-6 ${stat.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Live Auctions */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Gavel className="h-5 w-5 text-primary" />
                Live Auctions
              </CardTitle>
              <CardDescription>Bid on artworks from talented artists across India</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {liveAuctions.map((auction) => (
                <div key={auction.id} className="flex gap-4 p-4 border rounded-lg">
                  <img
                    src={auction.image || "/placeholder.svg"}
                    alt={auction.title}
                    className="w-32 h-24 object-cover rounded-lg shrink-0"
                  />
                  <div className="flex-1 space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium text-balance">{auction.title}</h4>
                        <p className="text-sm text-muted-foreground">by {auction.artist}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {auction.category}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Current Bid</p>
                        <p className="font-bold text-lg text-primary">{auction.currentBid}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Starting Bid</p>
                        <p className="font-medium">{auction.startingBid}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Timer className="h-3 w-3" />
                          {auction.timeLeft}
                        </span>
                        <span className="flex items-center gap-1">
                          <Users className="h-3 w-3" />
                          {auction.bidders} bidders
                        </span>
                        <span className="flex items-center gap-1">
                          <Eye className="h-3 w-3" />
                          {auction.views}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <Button size="sm" variant="outline">
                          Watch
                        </Button>
                        <Button size="sm">Place Bid</Button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* My Auctions */}
          <Card>
            <CardHeader>
              <CardTitle>My Auctions</CardTitle>
              <CardDescription>Track your listed artworks and sales</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {myAuctions.map((auction) => (
                <div key={auction.id} className="p-4 border rounded-lg space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">{auction.title}</h4>
                    <Badge variant={auction.status === "Active" ? "default" : "secondary"}>{auction.status}</Badge>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">
                        {auction.status === "Active" ? "Current Bid" : "Final Bid"}
                      </p>
                      <p className="font-bold text-lg">
                        {auction.status === "Active" ? auction.currentBid : auction.finalBid}
                      </p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Starting Bid</p>
                      <p className="font-medium">{auction.startingBid}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">{auction.status === "Active" ? "Time Left" : "Sold Date"}</p>
                      <p className="font-medium">{auction.status === "Active" ? auction.timeLeft : auction.soldDate}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span>{auction.bidders} bidders</span>
                      <span>{auction.views} views</span>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        View Details
                      </Button>
                      {auction.status === "Active" && (
                        <Button size="sm" variant="outline">
                          Edit
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full gap-2">
                <Gavel className="h-4 w-4" />
                List New Artwork
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Eye className="h-4 w-4" />
                Browse Auctions
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Heart className="h-4 w-4" />
                My Watchlist
              </Button>
            </CardContent>
          </Card>

          {/* Trending Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Trending Categories</CardTitle>
              <CardDescription>Popular art styles this week</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div>
                  <p className="font-medium text-sm">Traditional Madhubani</p>
                  <p className="text-xs text-muted-foreground">45 active auctions</p>
                </div>
                <Badge variant="default" className="text-xs">
                  Hot
                </Badge>
              </div>
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div>
                  <p className="font-medium text-sm">Digital Art</p>
                  <p className="text-xs text-muted-foreground">32 active auctions</p>
                </div>
                <Badge variant="secondary" className="text-xs">
                  Rising
                </Badge>
              </div>
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div>
                  <p className="font-medium text-sm">Tanjore Paintings</p>
                  <p className="text-xs text-muted-foreground">28 active auctions</p>
                </div>
                <Badge variant="outline" className="text-xs">
                  Stable
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Auction Tips */}
          <Card>
            <CardHeader>
              <CardTitle>Auction Tips</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm">
              <div className="p-3 bg-muted/50 rounded-lg">
                <p className="font-medium mb-1">Set Reserve Price</p>
                <p className="text-muted-foreground text-xs">Protect your artwork with a minimum selling price</p>
              </div>
              <div className="p-3 bg-muted/50 rounded-lg">
                <p className="font-medium mb-1">High-Quality Photos</p>
                <p className="text-muted-foreground text-xs">Clear, well-lit images increase bidding activity</p>
              </div>
              <div className="p-3 bg-muted/50 rounded-lg">
                <p className="font-medium mb-1">Optimal Timing</p>
                <p className="text-muted-foreground text-xs">End auctions on weekends for maximum visibility</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
