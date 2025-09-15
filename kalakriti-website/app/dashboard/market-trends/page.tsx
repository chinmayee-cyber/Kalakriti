"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import { TrendingUp, TrendingDown, Eye, Heart, Share2, Calendar, Target, Lightbulb } from "lucide-react"

const trendingStyles = [
  {
    name: "Contemporary Madhubani",
    growth: "+45%",
    trend: "up",
    popularity: 85,
    description: "Modern interpretations of traditional Madhubani art are gaining global attention",
    color: "bg-green-500",
  },
  {
    name: "Digital Warli Art",
    growth: "+32%",
    trend: "up",
    popularity: 72,
    description: "Traditional Warli paintings adapted for digital platforms",
    color: "bg-blue-500",
  },
  {
    name: "Fusion Tanjore",
    growth: "+28%",
    trend: "up",
    popularity: 68,
    description: "Classical Tanjore paintings with contemporary themes",
    color: "bg-purple-500",
  },
  {
    name: "Miniature Portraits",
    growth: "-12%",
    trend: "down",
    popularity: 45,
    description: "Traditional miniature painting style seeing reduced demand",
    color: "bg-orange-500",
  },
]

const marketInsights = [
  {
    title: "Peak Selling Season",
    value: "Oct - Dec",
    description: "Festival season shows 3x higher sales",
    icon: Calendar,
  },
  {
    title: "Top Buyer Demographics",
    value: "25-45 years",
    description: "Urban professionals are primary buyers",
    icon: Target,
  },
  {
    title: "Engagement Rate",
    value: "4.2%",
    description: "Average social media engagement",
    icon: Heart,
  },
  {
    title: "Price Range Sweet Spot",
    value: "₹5K - ₹25K",
    description: "Optimal pricing for maximum sales",
    icon: TrendingUp,
  },
]

const recommendations = [
  {
    title: "Focus on Contemporary Madhubani",
    description: "This style is trending upward with 45% growth. Consider creating pieces in this style.",
    priority: "High",
    impact: "Revenue +30%",
  },
  {
    title: "Optimize for Festival Season",
    description: "Prepare inventory for Oct-Dec period when sales are 3x higher.",
    priority: "Medium",
    impact: "Sales +200%",
  },
  {
    title: "Target Urban Professionals",
    description: "Focus marketing efforts on 25-45 age group in urban areas.",
    priority: "High",
    impact: "Reach +150%",
  },
]

export default function MarketTrendsPage() {
  return (
    <DashboardLayout
      title="Market Trend Analysis"
      description="AI-powered insights into art market trends and opportunities"
    >
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {marketInsights.map((insight, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <insight.icon className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <div className="text-2xl font-bold">{insight.value}</div>
                  <p className="text-sm font-medium">{insight.title}</p>
                  <p className="text-xs text-muted-foreground">{insight.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trending Art Styles */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-primary" />
              Trending Art Styles
            </CardTitle>
            <CardDescription>Current market trends and style popularity</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {trendingStyles.map((style, index) => (
              <div key={index} className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`${style.color} w-3 h-3 rounded-full`} />
                    <div>
                      <p className="font-medium">{style.name}</p>
                      <p className="text-sm text-muted-foreground">{style.description}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {style.trend === "up" ? (
                      <TrendingUp className="h-4 w-4 text-green-500" />
                    ) : (
                      <TrendingDown className="h-4 w-4 text-red-500" />
                    )}
                    <Badge variant={style.trend === "up" ? "default" : "destructive"} className="text-xs">
                      {style.growth}
                    </Badge>
                  </div>
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Popularity</span>
                    <span>{style.popularity}%</span>
                  </div>
                  <Progress value={style.popularity} className="h-2" />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* AI Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lightbulb className="h-5 w-5 text-primary" />
              AI Recommendations
            </CardTitle>
            <CardDescription>Personalized suggestions to boost your art sales</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recommendations.map((rec, index) => (
              <div key={index} className="p-4 border rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">{rec.title}</h4>
                  <Badge variant={rec.priority === "High" ? "default" : "secondary"} className="text-xs">
                    {rec.priority}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground">{rec.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-green-600">{rec.impact}</span>
                  <Button size="sm" variant="outline">
                    Apply
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Market Performance */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Market Performance Overview</CardTitle>
          <CardDescription>Key metrics and performance indicators</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
              <Eye className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-green-700">2.4M</div>
              <p className="text-sm text-green-600">Total Views This Month</p>
            </div>
            <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg">
              <Heart className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-700">156K</div>
              <p className="text-sm text-blue-600">Likes & Favorites</p>
            </div>
            <div className="text-center p-6 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
              <Share2 className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-purple-700">89K</div>
              <p className="text-sm text-purple-600">Shares & Reposts</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </DashboardLayout>
  )
}
