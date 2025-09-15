"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import {
  Instagram,
  Facebook,
  Twitter,
  Youtube,
  Heart,
  MessageCircle,
  Share2,
  Calendar,
  Zap,
  Target,
  BarChart3,
} from "lucide-react"

const socialPlatforms = [
  {
    name: "Instagram",
    icon: Instagram,
    followers: "12.5K",
    engagement: "4.2%",
    posts: 156,
    growth: "+15%",
    color: "bg-pink-500",
    connected: true,
  },
  {
    name: "Facebook",
    icon: Facebook,
    followers: "8.3K",
    engagement: "3.1%",
    posts: 89,
    growth: "+8%",
    color: "bg-blue-600",
    connected: true,
  },
  {
    name: "Twitter",
    icon: Twitter,
    followers: "5.2K",
    engagement: "2.8%",
    posts: 234,
    growth: "+12%",
    color: "bg-sky-500",
    connected: false,
  },
  {
    name: "YouTube",
    icon: Youtube,
    followers: "3.1K",
    engagement: "6.5%",
    posts: 24,
    growth: "+22%",
    color: "bg-red-500",
    connected: false,
  },
]

const contentSuggestions = [
  {
    type: "Behind the Scenes",
    description: "Show your painting process with time-lapse videos",
    engagement: "High",
    bestTime: "6-8 PM",
    platforms: ["Instagram", "Facebook"],
    hashtags: "#ArtProcess #IndianArt #Madhubani",
  },
  {
    type: "Art Tutorial",
    description: "Step-by-step guide for basic Warli patterns",
    engagement: "Very High",
    bestTime: "2-4 PM",
    platforms: ["YouTube", "Instagram"],
    hashtags: "#ArtTutorial #WarliArt #LearnArt",
  },
  {
    type: "Cultural Story",
    description: "Share the history behind your art style",
    engagement: "Medium",
    bestTime: "7-9 AM",
    platforms: ["Facebook", "Twitter"],
    hashtags: "#ArtHistory #Culture #Tradition",
  },
]

const scheduledPosts = [
  {
    id: 1,
    title: "New Madhubani painting completed!",
    platform: "Instagram",
    scheduledFor: "Today, 6:00 PM",
    status: "scheduled",
    engagement: "Predicted: 450 likes",
  },
  {
    id: 2,
    title: "Art tutorial: Basic brush techniques",
    platform: "YouTube",
    scheduledFor: "Tomorrow, 3:00 PM",
    status: "draft",
    engagement: "Predicted: 1.2K views",
  },
  {
    id: 3,
    title: "Behind the scenes: Studio setup",
    platform: "Facebook",
    scheduledFor: "Dec 18, 7:00 PM",
    status: "scheduled",
    engagement: "Predicted: 280 reactions",
  },
]

const campaignMetrics = [
  {
    title: "Reach",
    value: "45.2K",
    change: "+18%",
    icon: Target,
    color: "text-blue-600",
  },
  {
    title: "Engagement",
    value: "3.8K",
    change: "+25%",
    icon: Heart,
    color: "text-pink-600",
  },
  {
    title: "Shares",
    value: "892",
    change: "+12%",
    icon: Share2,
    color: "text-green-600",
  },
  {
    title: "Comments",
    value: "456",
    change: "+8%",
    icon: MessageCircle,
    color: "text-purple-600",
  },
]

export default function SocialPromotionPage() {
  return (
    <DashboardLayout
      title="AI-Powered Social Promotion"
      description="Intelligent strategies to maximize your art visibility across social platforms"
    >
      {/* Campaign Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {campaignMetrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
                  <div className="text-2xl font-bold">{metric.value}</div>
                  <p className={`text-sm ${metric.color}`}>{metric.change} from last month</p>
                </div>
                <div className={`p-3 rounded-lg bg-muted`}>
                  <metric.icon className={`h-6 w-6 ${metric.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Social Platforms */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                Social Platform Performance
              </CardTitle>
              <CardDescription>Overview of your presence across different platforms</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {socialPlatforms.map((platform, index) => (
                <div key={index} className="flex items-center gap-4 p-4 border rounded-lg">
                  <div className={`${platform.color} p-3 rounded-lg text-white`}>
                    <platform.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{platform.name}</h4>
                      <div className="flex items-center gap-2">
                        <Badge variant={platform.connected ? "default" : "secondary"}>
                          {platform.connected ? "Connected" : "Not Connected"}
                        </Badge>
                        <Badge variant="outline" className="text-green-600">
                          {platform.growth}
                        </Badge>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Followers</p>
                        <p className="font-medium">{platform.followers}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Engagement</p>
                        <p className="font-medium">{platform.engagement}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Posts</p>
                        <p className="font-medium">{platform.posts}</p>
                      </div>
                    </div>
                  </div>
                  <Button size="sm" variant={platform.connected ? "outline" : "default"}>
                    {platform.connected ? "Manage" : "Connect"}
                  </Button>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Content Suggestions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                AI Content Suggestions
              </CardTitle>
              <CardDescription>Personalized content ideas to boost engagement</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {contentSuggestions.map((suggestion, index) => (
                <div key={index} className="p-4 border rounded-lg space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">{suggestion.type}</h4>
                    <Badge
                      variant={
                        suggestion.engagement === "Very High"
                          ? "default"
                          : suggestion.engagement === "High"
                            ? "secondary"
                            : "outline"
                      }
                    >
                      {suggestion.engagement} Engagement
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{suggestion.description}</p>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      Best time: {suggestion.bestTime}
                    </span>
                    <span>Platforms: {suggestion.platforms.join(", ")}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <p className="text-xs text-muted-foreground">{suggestion.hashtags}</p>
                    <Button size="sm" variant="outline">
                      Create Post
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Scheduled Posts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Scheduled Posts
              </CardTitle>
              <CardDescription>Your upcoming content</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {scheduledPosts.map((post) => (
                <div key={post.id} className="p-3 border rounded-lg space-y-2">
                  <div className="flex items-center justify-between">
                    <h5 className="font-medium text-sm text-balance">{post.title}</h5>
                    <Badge variant={post.status === "scheduled" ? "default" : "secondary"} className="text-xs">
                      {post.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{post.platform}</p>
                  <p className="text-xs text-muted-foreground">{post.scheduledFor}</p>
                  <p className="text-xs text-green-600">{post.engagement}</p>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" className="text-xs h-7 bg-transparent">
                      Edit
                    </Button>
                    <Button size="sm" variant="outline" className="text-xs h-7 bg-transparent">
                      Preview
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Engagement Trends */}
          <Card>
            <CardHeader>
              <CardTitle>Engagement Trends</CardTitle>
              <CardDescription>Best performing content types</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Art Process Videos</span>
                  <span>85%</span>
                </div>
                <Progress value={85} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Finished Artwork</span>
                  <span>72%</span>
                </div>
                <Progress value={72} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Cultural Stories</span>
                  <span>68%</span>
                </div>
                <Progress value={68} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Art Tutorials</span>
                  <span>91%</span>
                </div>
                <Progress value={91} className="h-2" />
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full gap-2">
                <Zap className="h-4 w-4" />
                Generate Post
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Calendar className="h-4 w-4" />
                Schedule Content
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <BarChart3 className="h-4 w-4" />
                View Analytics
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
