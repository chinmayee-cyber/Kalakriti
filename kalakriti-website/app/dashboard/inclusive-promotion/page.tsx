"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Users, Heart, Award, Megaphone, HandHeart, Star, Calendar, TrendingUp, UserCheck, Gift } from "lucide-react"

const supportPrograms = [
  {
    id: 1,
    title: "Women Artists Empowerment",
    description: "Special support and promotion for women artists",
    participants: 450,
    grants: "₹12,50,000",
    successRate: "92%",
    color: "bg-pink-500",
    icon: Heart,
  },
  {
    id: 2,
    title: "Differently-Abled Creators",
    description: "Inclusive platform for artists with disabilities",
    participants: 180,
    grants: "₹8,75,000",
    successRate: "88%",
    color: "bg-blue-500",
    icon: HandHeart,
  },
  {
    id: 3,
    title: "Rural Artist Initiative",
    description: "Supporting artists from remote villages",
    participants: 320,
    grants: "₹15,25,000",
    successRate: "85%",
    color: "bg-green-500",
    icon: Users,
  },
  {
    id: 4,
    title: "Youth Art Program",
    description: "Encouraging young artists under 25",
    participants: 280,
    grants: "₹6,80,000",
    successRate: "90%",
    color: "bg-purple-500",
    icon: Star,
  },
]

const featuredArtists = [
  {
    id: 1,
    name: "Priya Sharma",
    location: "Madhubani, Bihar",
    category: "Women Artist",
    artStyle: "Traditional Madhubani",
    sales: "₹45,000",
    growth: "+35%",
    image: "/placeholder.svg?key=artist1",
    story: "Empowering women through traditional art forms",
  },
  {
    id: 2,
    name: "Ravi Kumar",
    location: "Udaipur, Rajasthan",
    category: "Differently-Abled",
    artStyle: "Miniature Paintings",
    sales: "₹32,000",
    growth: "+28%",
    image: "/placeholder.svg?key=artist2",
    story: "Creating beautiful art despite physical challenges",
  },
  {
    id: 3,
    name: "Meera Devi",
    location: "Warli Village, Maharashtra",
    category: "Rural Artist",
    artStyle: "Warli Art",
    sales: "₹28,500",
    growth: "+42%",
    image: "/placeholder.svg?key=artist3",
    story: "Bringing village art to global platforms",
  },
]

const upcomingEvents = [
  {
    title: "Women Artists Exhibition",
    date: "Dec 20, 2024",
    location: "Mumbai Art Gallery",
    participants: 25,
    type: "Exhibition",
  },
  {
    title: "Inclusive Art Workshop",
    date: "Dec 25, 2024",
    location: "Online",
    participants: 50,
    type: "Workshop",
  },
  {
    title: "Rural Art Fair",
    date: "Jan 5, 2025",
    location: "Delhi",
    participants: 40,
    type: "Fair",
  },
]

const impactMetrics = [
  {
    title: "Artists Supported",
    value: "1,230",
    change: "+18%",
    icon: Users,
    color: "text-blue-600",
  },
  {
    title: "Grants Distributed",
    value: "₹43.3L",
    change: "+25%",
    icon: Gift,
    color: "text-green-600",
  },
  {
    title: "Success Stories",
    value: "89%",
    change: "+12%",
    icon: Award,
    color: "text-purple-600",
  },
  {
    title: "Community Reach",
    value: "25K+",
    change: "+30%",
    icon: Megaphone,
    color: "text-orange-600",
  },
]

export default function InclusivePromotionPage() {
  return (
    <DashboardLayout
      title="Inclusive Art Promotion"
      description="Dedicated support and promotion for women artists and differently-abled creators"
    >
      {/* Impact Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {impactMetrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
                  <div className="text-2xl font-bold">{metric.value}</div>
                  <p className={`text-sm ${metric.color}`}>{metric.change} this year</p>
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
        {/* Support Programs */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <HandHeart className="h-5 w-5 text-primary" />
                Support Programs
              </CardTitle>
              <CardDescription>Inclusive initiatives empowering diverse artists</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {supportPrograms.map((program) => (
                <div key={program.id} className="p-4 border rounded-lg space-y-4">
                  <div className="flex items-start gap-4">
                    <div className={`${program.color} p-3 rounded-lg text-white`}>
                      <program.icon className="h-6 w-6" />
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-balance">{program.title}</h4>
                      <p className="text-sm text-muted-foreground">{program.description}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">Participants</p>
                      <p className="font-bold text-lg">{program.participants}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Grants Given</p>
                      <p className="font-bold text-lg">{program.grants}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Success Rate</p>
                      <p className="font-bold text-lg text-green-600">{program.successRate}</p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      Learn More
                    </Button>
                    <Button size="sm">Apply Now</Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Featured Artists */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Star className="h-5 w-5 text-primary" />
                Featured Success Stories
              </CardTitle>
              <CardDescription>Artists who have thrived through our inclusive programs</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {featuredArtists.map((artist) => (
                <div key={artist.id} className="flex gap-4 p-4 border rounded-lg">
                  <img
                    src={artist.image || "/placeholder.svg"}
                    alt={artist.name}
                    className="w-20 h-20 object-cover rounded-full shrink-0"
                  />
                  <div className="flex-1 space-y-2">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium">{artist.name}</h4>
                        <p className="text-sm text-muted-foreground">{artist.location}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {artist.category}
                      </Badge>
                    </div>

                    <p className="text-sm text-muted-foreground italic">"{artist.story}"</p>

                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Art Style</p>
                        <p className="font-medium">{artist.artStyle}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Total Sales</p>
                        <p className="font-medium">{artist.sales}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Growth</p>
                        <p className="font-medium text-green-600">{artist.growth}</p>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        View Profile
                      </Button>
                      <Button size="sm" variant="outline">
                        View Art
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Apply for Support */}
          <Card>
            <CardHeader>
              <CardTitle>Apply for Support</CardTitle>
              <CardDescription>Get personalized assistance</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button className="w-full gap-2">
                <UserCheck className="h-4 w-4" />
                Apply for Grant
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Megaphone className="h-4 w-4" />
                Request Promotion
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Award className="h-4 w-4" />
                Join Mentorship
              </Button>
            </CardContent>
          </Card>

          {/* Upcoming Events */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-primary" />
                Upcoming Events
              </CardTitle>
              <CardDescription>Inclusive art events and workshops</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {upcomingEvents.map((event, index) => (
                <div key={index} className="p-3 border rounded-lg space-y-2">
                  <div className="flex items-center justify-between">
                    <h5 className="font-medium text-sm text-balance">{event.title}</h5>
                    <Badge variant="outline" className="text-xs">
                      {event.type}
                    </Badge>
                  </div>
                  <p className="text-xs text-muted-foreground">{event.date}</p>
                  <p className="text-xs text-muted-foreground">{event.location}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">{event.participants} participants</span>
                    <Button size="sm" variant="outline" className="text-xs h-7 bg-transparent">
                      Register
                    </Button>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Community Impact */}
          <Card>
            <CardHeader>
              <CardTitle>Community Impact</CardTitle>
              <CardDescription>Your contribution to inclusive art</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-center p-4 bg-gradient-to-r from-pink-50 to-pink-100 rounded-lg">
                <Heart className="h-8 w-8 text-pink-600 mx-auto mb-2" />
                <div className="text-2xl font-bold text-pink-700">15</div>
                <p className="text-sm text-pink-600">Artists you've supported</p>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Women Artists</span>
                  <span>60%</span>
                </div>
                <Progress value={60} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Differently-Abled</span>
                  <span>25%</span>
                </div>
                <Progress value={25} className="h-2" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Rural Artists</span>
                  <span>40%</span>
                </div>
                <Progress value={40} className="h-2" />
              </div>
            </CardContent>
          </Card>

          {/* Resources */}
          <Card>
            <CardHeader>
              <CardTitle>Resources</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full gap-2 justify-start bg-transparent">
                <Award className="h-4 w-4" />
                Grant Guidelines
              </Button>
              <Button variant="outline" className="w-full gap-2 justify-start bg-transparent">
                <Users className="h-4 w-4" />
                Community Forum
              </Button>
              <Button variant="outline" className="w-full gap-2 justify-start bg-transparent">
                <TrendingUp className="h-4 w-4" />
                Success Stories
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
