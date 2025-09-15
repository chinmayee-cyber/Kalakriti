"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import {
  GraduationCap,
  Play,
  Clock,
  Users,
  Star,
  BookOpen,
  Award,
  Video,
  Palette,
  Brush,
  ImageIcon,
} from "lucide-react"

const featuredCourses = [
  {
    id: 1,
    title: "Madhubani Painting Masterclass",
    instructor: "Sita Devi",
    duration: "6 weeks",
    students: 1250,
    rating: 4.9,
    progress: 0,
    level: "Beginner",
    thumbnail: "/madhubani-painting-colorful-traditional.jpg",
    description: "Learn the traditional art of Madhubani painting with modern techniques",
    lessons: 24,
    category: "Traditional Art",
  },
  {
    id: 2,
    title: "Digital Art for Traditional Artists",
    instructor: "Raj Kumar",
    duration: "4 weeks",
    students: 890,
    rating: 4.7,
    progress: 65,
    level: "Intermediate",
    thumbnail: "/placeholder-tiv7h.png",
    description: "Bridge traditional skills with digital art tools and techniques",
    lessons: 18,
    category: "Digital Art",
  },
  {
    id: 3,
    title: "Warli Art: From Village to Gallery",
    instructor: "Meera Patil",
    duration: "5 weeks",
    students: 675,
    rating: 4.8,
    progress: 30,
    level: "Beginner",
    thumbnail: "/placeholder-o3xqp.png",
    description: "Master the ancient Warli art form and prepare for gallery exhibitions",
    lessons: 20,
    category: "Traditional Art",
  },
]

const skillCategories = [
  {
    name: "Traditional Techniques",
    courses: 45,
    icon: Brush,
    color: "bg-orange-500",
    description: "Master classical Indian art forms",
  },
  {
    name: "Digital Art",
    courses: 32,
    icon: ImageIcon,
    color: "bg-blue-500",
    description: "Modern digital painting and design",
  },
  {
    name: "Business Skills",
    courses: 28,
    icon: Award,
    color: "bg-green-500",
    description: "Art marketing and entrepreneurship",
  },
  {
    name: "Art History",
    courses: 22,
    icon: BookOpen,
    color: "bg-purple-500",
    description: "Cultural context and art movements",
  },
]

const achievements = [
  {
    title: "First Course Completed",
    description: "Completed your first art course",
    earned: true,
    icon: GraduationCap,
  },
  {
    title: "Traditional Master",
    description: "Completed 5 traditional art courses",
    earned: true,
    icon: Palette,
  },
  {
    title: "Digital Pioneer",
    description: "Completed 3 digital art courses",
    earned: false,
    icon: Video,
  },
  {
    title: "Community Contributor",
    description: "Helped 10 fellow students",
    earned: false,
    icon: Users,
  },
]

export default function ArtEducationPage() {
  return (
    <DashboardLayout
      title="Art Education Platform"
      description="Comprehensive learning platform for traditional and modern art techniques"
    >
      {/* Learning Progress Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-primary mb-2">3</div>
            <p className="text-sm font-medium">Courses Enrolled</p>
            <p className="text-xs text-muted-foreground">2 in progress</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">1</div>
            <p className="text-sm font-medium">Courses Completed</p>
            <p className="text-xs text-muted-foreground">Certificate earned</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">42h</div>
            <p className="text-sm font-medium">Learning Time</p>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">85%</div>
            <p className="text-sm font-medium">Average Score</p>
            <p className="text-xs text-muted-foreground">Across all courses</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* My Courses */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <GraduationCap className="h-5 w-5 text-primary" />
                My Courses
              </CardTitle>
              <CardDescription>Continue your learning journey</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {featuredCourses.map((course) => (
                <div key={course.id} className="flex gap-4 p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                  <img
                    src={course.thumbnail || "/placeholder.svg"}
                    alt={course.title}
                    className="w-24 h-16 object-cover rounded-lg shrink-0"
                  />
                  <div className="flex-1 space-y-2">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium text-balance">{course.title}</h4>
                        <p className="text-sm text-muted-foreground">by {course.instructor}</p>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {course.level}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {course.duration}
                      </span>
                      <span className="flex items-center gap-1">
                        <Users className="h-3 w-3" />
                        {course.students}
                      </span>
                      <span className="flex items-center gap-1">
                        <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                        {course.rating}
                      </span>
                    </div>
                    {course.progress > 0 && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-sm">
                          <span>Progress</span>
                          <span>{course.progress}%</span>
                        </div>
                        <Progress value={course.progress} className="h-2" />
                      </div>
                    )}
                    <div className="flex items-center gap-2">
                      <Button size="sm" className="gap-1">
                        <Play className="h-3 w-3" />
                        {course.progress > 0 ? "Continue" : "Start Course"}
                      </Button>
                      <Button size="sm" variant="outline">
                        View Details
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Skill Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Explore by Category</CardTitle>
              <CardDescription>Discover courses in different art disciplines</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {skillCategories.map((category, index) => (
                  <div key={index} className="p-4 border rounded-lg hover:bg-muted/50 transition-colors cursor-pointer">
                    <div className="flex items-center gap-3 mb-2">
                      <div className={`${category.color} p-2 rounded-lg text-white`}>
                        <category.icon className="h-5 w-5" />
                      </div>
                      <div>
                        <h4 className="font-medium">{category.name}</h4>
                        <p className="text-sm text-muted-foreground">{category.courses} courses</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">{category.description}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Achievements */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5 text-primary" />
                Achievements
              </CardTitle>
              <CardDescription>Your learning milestones</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {achievements.map((achievement, index) => (
                <div
                  key={index}
                  className={`flex items-center gap-3 p-3 rounded-lg ${
                    achievement.earned ? "bg-green-50 border border-green-200" : "bg-muted/50"
                  }`}
                >
                  <div
                    className={`p-2 rounded-lg ${
                      achievement.earned ? "bg-green-500 text-white" : "bg-muted text-muted-foreground"
                    }`}
                  >
                    <achievement.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <p className={`text-sm font-medium ${achievement.earned ? "text-green-700" : ""}`}>
                      {achievement.title}
                    </p>
                    <p className="text-xs text-muted-foreground">{achievement.description}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Learning Streak */}
          <Card>
            <CardHeader>
              <CardTitle>Learning Streak</CardTitle>
              <CardDescription>Keep up the momentum!</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-primary mb-2">7</div>
              <p className="text-sm font-medium mb-4">Days in a row</p>
              <div className="flex justify-center gap-1 mb-4">
                {[...Array(7)].map((_, i) => (
                  <div key={i} className="w-3 h-3 bg-primary rounded-full" />
                ))}
              </div>
              <Button size="sm" className="w-full">
                Continue Streak
              </Button>
            </CardContent>
          </Card>

          {/* Recommended Course */}
          <Card>
            <CardHeader>
              <CardTitle>Recommended for You</CardTitle>
            </CardHeader>
            <CardContent>
              <img
                src="/tanjore-painting-gold-traditional.jpg"
                alt="Recommended course"
                className="w-full h-24 object-cover rounded-lg mb-3"
              />
              <h4 className="font-medium mb-1">Tanjore Painting Techniques</h4>
              <p className="text-sm text-muted-foreground mb-3">Master the art of gold leaf application</p>
              <Button size="sm" className="w-full">
                Enroll Now
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
