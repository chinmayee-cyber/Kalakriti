"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Eye, Play, Volume2, Download, Share2, Wand2, FileVideo, Headphones, Languages } from "lucide-react"

const artworks = [
  {
    id: 1,
    title: "Madhubani Village Festival",
    originalImage: "/placeholder.svg?key=multi1",
    hasVideo: true,
    hasAudio: true,
    hasDescription: true,
    languages: ["Hindi", "English", "Bengali"],
    views: 1250,
    status: "Complete",
    processingTime: "2 minutes",
  },
  {
    id: 2,
    title: "Warli Tribal Dance",
    originalImage: "/placeholder.svg?key=multi2",
    hasVideo: false,
    hasAudio: true,
    hasDescription: true,
    languages: ["Hindi", "English"],
    views: 890,
    status: "Processing",
    processingTime: "5 minutes",
    progress: 65,
  },
  {
    id: 3,
    title: "Tanjore Krishna Portrait",
    originalImage: "/placeholder.svg?key=multi3",
    hasVideo: true,
    hasAudio: false,
    hasDescription: true,
    languages: ["Hindi", "English", "Tamil"],
    views: 2100,
    status: "Complete",
    processingTime: "3 minutes",
  },
]

const features = [
  {
    title: "Video Transformation",
    description: "Convert static paintings into dynamic video experiences",
    icon: FileVideo,
    color: "bg-blue-500",
    usage: "12 artworks transformed",
  },
  {
    title: "Audio Descriptions",
    description: "AI-generated audio descriptions for accessibility",
    icon: Headphones,
    color: "bg-green-500",
    usage: "18 descriptions created",
  },
  {
    title: "Multi-language Support",
    description: "Descriptions available in multiple Indian languages",
    icon: Languages,
    color: "bg-purple-500",
    usage: "8 languages supported",
  },
  {
    title: "Interactive Elements",
    description: "Add clickable hotspots and information layers",
    icon: Wand2,
    color: "bg-orange-500",
    usage: "25 interactive elements",
  },
]

const accessibilityMetrics = [
  {
    title: "Accessibility Score",
    value: "95%",
    change: "+8%",
    icon: Eye,
    color: "text-green-600",
  },
  {
    title: "Audio Descriptions",
    value: "18",
    change: "+6",
    icon: Volume2,
    color: "text-blue-600",
  },
  {
    title: "Video Views",
    value: "4.2K",
    change: "+25%",
    icon: Play,
    color: "text-purple-600",
  },
  {
    title: "Downloads",
    value: "892",
    change: "+15%",
    icon: Download,
    color: "text-orange-600",
  },
]

export default function MultimodalExperiencePage() {
  return (
    <DashboardLayout
      title="Multimodal Art Experience"
      description="Transform paintings into videos, audio descriptions for accessibility and enhanced engagement"
    >
      {/* Accessibility Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {accessibilityMetrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
                  <div className="text-2xl font-bold">{metric.value}</div>
                  <p className={`text-sm ${metric.color}`}>{metric.change} this month</p>
                </div>
                <div className="p-3 rounded-lg bg-muted">
                  <metric.icon className={`h-6 w-6 ${metric.color}`} />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Artwork Transformations */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5 text-primary" />
                Multimodal Artworks
              </CardTitle>
              <CardDescription>Your artworks enhanced with video, audio, and interactive elements</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {artworks.map((artwork) => (
                <div key={artwork.id} className="p-4 border rounded-lg space-y-4">
                  <div className="flex gap-4">
                    <img
                      src={artwork.originalImage || "/placeholder.svg"}
                      alt={artwork.title}
                      className="w-32 h-24 object-cover rounded-lg shrink-0"
                    />
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <h4 className="font-medium text-balance">{artwork.title}</h4>
                          <p className="text-sm text-muted-foreground">{artwork.views} views</p>
                        </div>
                        <Badge variant={artwork.status === "Complete" ? "default" : "secondary"}>
                          {artwork.status}
                        </Badge>
                      </div>

                      {artwork.status === "Processing" && artwork.progress && (
                        <div className="space-y-1">
                          <div className="flex justify-between text-sm">
                            <span>Processing</span>
                            <span>{artwork.progress}%</span>
                          </div>
                          <Progress value={artwork.progress} className="h-2" />
                          <p className="text-xs text-muted-foreground">Estimated time: {artwork.processingTime}</p>
                        </div>
                      )}

                      <div className="flex items-center gap-2">
                        {artwork.hasVideo && (
                          <Badge variant="outline" className="text-xs gap-1">
                            <FileVideo className="h-3 w-3" />
                            Video
                          </Badge>
                        )}
                        {artwork.hasAudio && (
                          <Badge variant="outline" className="text-xs gap-1">
                            <Volume2 className="h-3 w-3" />
                            Audio
                          </Badge>
                        )}
                        {artwork.hasDescription && (
                          <Badge variant="outline" className="text-xs gap-1">
                            <Languages className="h-3 w-3" />
                            {artwork.languages.length} languages
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span>Languages: {artwork.languages.join(", ")}</span>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline" className="gap-1 bg-transparent">
                        <Play className="h-3 w-3" />
                        Preview
                      </Button>
                      <Button size="sm" variant="outline" className="gap-1 bg-transparent">
                        <Share2 className="h-3 w-3" />
                        Share
                      </Button>
                      <Button size="sm" className="gap-1">
                        <Download className="h-3 w-3" />
                        Download
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Features Overview */}
          <Card>
            <CardHeader>
              <CardTitle>Multimodal Features</CardTitle>
              <CardDescription>Available transformation and accessibility features</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {features.map((feature, index) => (
                  <div key={index} className="p-4 border rounded-lg">
                    <div className="flex items-center gap-3 mb-3">
                      <div className={`${feature.color} p-2 rounded-lg text-white`}>
                        <feature.icon className="h-5 w-5" />
                      </div>
                      <div>
                        <h4 className="font-medium">{feature.title}</h4>
                        <p className="text-xs text-muted-foreground">{feature.usage}</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">{feature.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Transform */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Transform</CardTitle>
              <CardDescription>Transform your artwork instantly</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full gap-2">
                <Wand2 className="h-4 w-4" />
                Upload New Artwork
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <FileVideo className="h-4 w-4" />
                Create Video
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Volume2 className="h-4 w-4" />
                Generate Audio
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Languages className="h-4 w-4" />
                Add Languages
              </Button>
            </CardContent>
          </Card>

          {/* Accessibility Impact */}
          <Card>
            <CardHeader>
              <CardTitle>Accessibility Impact</CardTitle>
              <CardDescription>Your contribution to inclusive art</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
                <Eye className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-green-700">2,450</div>
                <p className="text-sm text-green-600">People reached with accessible content</p>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Visual Accessibility</span>
                  <span>95%</span>
                </div>
                <Progress value={95} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Audio Accessibility</span>
                  <span>88%</span>
                </div>
                <Progress value={88} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Language Coverage</span>
                  <span>72%</span>
                </div>
                <Progress value={72} className="h-2" />
              </div>
            </CardContent>
          </Card>

          {/* Processing Queue */}
          <Card>
            <CardHeader>
              <CardTitle>Processing Queue</CardTitle>
              <CardDescription>Upcoming transformations</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 border rounded-lg">
                <p className="font-medium text-sm">Warli Art Video</p>
                <p className="text-xs text-muted-foreground">Estimated: 3 minutes</p>
                <Progress value={65} className="h-2 mt-2" />
              </div>
              <div className="p-3 border rounded-lg">
                <p className="font-medium text-sm">Audio Description</p>
                <p className="text-xs text-muted-foreground">In queue</p>
                <Progress value={0} className="h-2 mt-2" />
              </div>
            </CardContent>
          </Card>

          {/* Language Support */}
          <Card>
            <CardHeader>
              <CardTitle>Supported Languages</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Hindi</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>English</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Bengali</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Tamil</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Telugu</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Marathi</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Gujarati</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full" />
                  <span>Punjabi</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
