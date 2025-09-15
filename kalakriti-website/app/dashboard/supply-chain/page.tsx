"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { DashboardLayout } from "@/components/dashboard-layout"
import { Package, MapPin, Star, Truck, Phone, Mail, Filter } from "lucide-react"

const suppliers = [
  {
    id: 1,
    name: "Rajesh Art Supplies",
    location: "Mumbai, Maharashtra",
    rating: 4.8,
    speciality: "Traditional Pigments",
    distance: "12 km",
    deliveryTime: "Same day",
    verified: true,
    products: ["Natural pigments", "Brushes", "Canvas"],
    contact: "+91 98765 43210",
  },
  {
    id: 2,
    name: "Heritage Craft Materials",
    location: "Jaipur, Rajasthan",
    rating: 4.6,
    speciality: "Gold Leaf & Foils",
    distance: "285 km",
    deliveryTime: "2-3 days",
    verified: true,
    products: ["Gold leaf", "Silver foil", "Adhesives"],
    contact: "+91 87654 32109",
  },
  {
    id: 3,
    name: "Eco Art Supplies",
    location: "Pune, Maharashtra",
    rating: 4.9,
    speciality: "Organic Materials",
    distance: "45 km",
    deliveryTime: "Next day",
    verified: true,
    products: ["Organic colors", "Bamboo brushes", "Handmade paper"],
    contact: "+91 76543 21098",
  },
]

const recentOrders = [
  {
    id: "ORD001",
    supplier: "Rajesh Art Supplies",
    items: "Natural pigments, Canvas",
    amount: "₹2,450",
    status: "Delivered",
    date: "Dec 10, 2024",
  },
  {
    id: "ORD002",
    supplier: "Heritage Craft Materials",
    items: "Gold leaf sheets",
    amount: "₹5,200",
    status: "In Transit",
    date: "Dec 12, 2024",
  },
  {
    id: "ORD003",
    supplier: "Eco Art Supplies",
    items: "Organic colors set",
    amount: "₹1,800",
    status: "Processing",
    date: "Dec 14, 2024",
  },
]

const categories = [
  { name: "Pigments & Colors", count: 45, icon: "🎨" },
  { name: "Brushes & Tools", count: 32, icon: "🖌️" },
  { name: "Canvas & Paper", count: 28, icon: "📄" },
  { name: "Gold & Silver Leaf", count: 15, icon: "✨" },
  { name: "Adhesives", count: 12, icon: "🔗" },
  { name: "Frames", count: 20, icon: "🖼️" },
]

export default function SupplyChainPage() {
  return (
    <DashboardLayout
      title="Supply Chain Network"
      description="Connect directly with verified material suppliers for seamless procurement"
    >
      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-primary mb-2">500+</div>
            <p className="text-sm font-medium">Verified Suppliers</p>
            <p className="text-xs text-muted-foreground">Across India</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">₹45K</div>
            <p className="text-sm font-medium">Total Savings</p>
            <p className="text-xs text-muted-foreground">This year</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">24</div>
            <p className="text-sm font-medium">Orders Placed</p>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">4.8</div>
            <p className="text-sm font-medium">Avg Rating</p>
            <p className="text-xs text-muted-foreground">Supplier quality</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Suppliers List */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Package className="h-5 w-5 text-primary" />
                    Recommended Suppliers
                  </CardTitle>
                  <CardDescription>Verified suppliers near your location</CardDescription>
                </div>
                <Button variant="outline" size="sm" className="gap-2 bg-transparent">
                  <Filter className="h-4 w-4" />
                  Filter
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {suppliers.map((supplier) => (
                <div key={supplier.id} className="p-4 border rounded-lg space-y-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-medium">{supplier.name}</h4>
                        {supplier.verified && (
                          <Badge variant="default" className="text-xs">
                            Verified
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <MapPin className="h-3 w-3" />
                          {supplier.location}
                        </span>
                        <span className="flex items-center gap-1">
                          <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                          {supplier.rating}
                        </span>
                      </div>
                    </div>
                    <div className="text-right text-sm">
                      <p className="font-medium">{supplier.distance}</p>
                      <p className="text-muted-foreground">{supplier.deliveryTime}</p>
                    </div>
                  </div>

                  <div>
                    <p className="text-sm font-medium mb-2">Speciality: {supplier.speciality}</p>
                    <div className="flex flex-wrap gap-2">
                      {supplier.products.map((product, index) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {product}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Phone className="h-3 w-3" />
                        {supplier.contact}
                      </span>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        Contact
                      </Button>
                      <Button size="sm">Order Now</Button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Orders */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Truck className="h-5 w-5 text-primary" />
                Recent Orders
              </CardTitle>
              <CardDescription>Track your recent material orders</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentOrders.map((order) => (
                <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <p className="font-medium">#{order.id}</p>
                      <Badge
                        variant={
                          order.status === "Delivered"
                            ? "default"
                            : order.status === "In Transit"
                              ? "secondary"
                              : "outline"
                        }
                        className="text-xs"
                      >
                        {order.status}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{order.supplier}</p>
                    <p className="text-sm">{order.items}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold">{order.amount}</p>
                    <p className="text-sm text-muted-foreground">{order.date}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Material Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Material Categories</CardTitle>
              <CardDescription>Browse by material type</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {categories.map((category, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{category.icon}</span>
                    <div>
                      <p className="font-medium text-sm">{category.name}</p>
                      <p className="text-xs text-muted-foreground">{category.count} suppliers</p>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Quick Order */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Order</CardTitle>
              <CardDescription>Reorder frequently used items</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-3 border rounded-lg">
                <p className="font-medium text-sm">Natural Pigment Set</p>
                <p className="text-xs text-muted-foreground">Last ordered: Dec 10</p>
                <Button size="sm" className="w-full mt-2">
                  Reorder - ₹2,450
                </Button>
              </div>
              <div className="p-3 border rounded-lg">
                <p className="font-medium text-sm">Canvas Bundle</p>
                <p className="text-xs text-muted-foreground">Last ordered: Nov 28</p>
                <Button size="sm" variant="outline" className="w-full mt-2 bg-transparent">
                  Reorder - ₹1,800
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Support */}
          <Card>
            <CardHeader>
              <CardTitle>Need Help?</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Phone className="h-4 w-4" />
                Call Support
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <Mail className="h-4 w-4" />
                Email Support
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
