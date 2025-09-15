"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { DashboardLayout } from "@/components/dashboard-layout"
import { DollarSign, TrendingUp, Shield, Coins, Wallet, FileText, CheckCircle, Clock } from "lucide-react"

const artPortfolio = [
  {
    id: 1,
    title: "Madhubani Village Scene",
    currentValue: "₹45,000",
    lastValuation: "₹42,000",
    change: "+7.1%",
    status: "Active",
    collateralUsed: "₹30,000",
    image: "/placeholder.svg?key=art1",
  },
  {
    id: 2,
    title: "Warli Tribal Dance",
    currentValue: "₹32,000",
    lastValuation: "₹35,000",
    change: "-8.6%",
    status: "Active",
    collateralUsed: "₹20,000",
    image: "/placeholder.svg?key=art2",
  },
  {
    id: 3,
    title: "Tanjore Krishna",
    currentValue: "₹78,000",
    lastValuation: "₹75,000",
    change: "+4.0%",
    status: "Pending",
    collateralUsed: "₹0",
    image: "/placeholder.svg?key=art3",
  },
]

const loanApplications = [
  {
    id: 1,
    amount: "₹25,000",
    purpose: "Art supplies and materials",
    collateral: "Madhubani Village Scene",
    status: "Approved",
    interestRate: "8.5%",
    term: "12 months",
  },
  {
    id: 2,
    amount: "₹15,000",
    purpose: "Studio rent",
    collateral: "Warli Tribal Dance",
    status: "Under Review",
    interestRate: "9.0%",
    term: "6 months",
  },
]

const valuationMetrics = [
  {
    title: "Total Portfolio Value",
    value: "₹1,55,000",
    change: "+12%",
    icon: Wallet,
    color: "text-green-600",
  },
  {
    title: "Available Collateral",
    value: "₹1,05,000",
    change: "+8%",
    icon: Shield,
    color: "text-blue-600",
  },
  {
    title: "Active Loans",
    value: "₹25,000",
    change: "0%",
    icon: Coins,
    color: "text-purple-600",
  },
  {
    title: "Credit Score",
    value: "785",
    change: "+15",
    icon: TrendingUp,
    color: "text-orange-600",
  },
]

export default function CryptoValuationPage() {
  return (
    <DashboardLayout
      title="Crypto Art Valuation"
      description="Blockchain-based art valuation system for collateral and micro-loans"
    >
      {/* Valuation Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        {valuationMetrics.map((metric, index) => (
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
        {/* Art Portfolio */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-primary" />
                Art Portfolio Valuation
              </CardTitle>
              <CardDescription>Real-time blockchain-based valuations of your artworks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {artPortfolio.map((art) => (
                <div key={art.id} className="flex gap-4 p-4 border rounded-lg">
                  <img
                    src={art.image || "/placeholder.svg"}
                    alt={art.title}
                    className="w-24 h-20 object-cover rounded-lg shrink-0"
                  />
                  <div className="flex-1 space-y-2">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium">{art.title}</h4>
                        <p className="text-sm text-muted-foreground">Current Valuation</p>
                      </div>
                      <Badge variant={art.status === "Active" ? "default" : "secondary"}>{art.status}</Badge>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Current Value</p>
                        <p className="font-bold text-lg">{art.currentValue}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Change</p>
                        <p className={`font-medium ${art.change.startsWith("+") ? "text-green-600" : "text-red-600"}`}>
                          {art.change}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Used as Collateral</p>
                        <p className="font-medium">{art.collateralUsed}</p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <Button size="sm" variant="outline">
                        Update Valuation
                      </Button>
                      <Button size="sm" variant="outline">
                        Use as Collateral
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Loan Applications */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-primary" />
                Micro-Loan Applications
              </CardTitle>
              <CardDescription>Track your loan applications using art as collateral</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {loanApplications.map((loan) => (
                <div key={loan.id} className="p-4 border rounded-lg space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">Loan Application #{loan.id}</h4>
                    <Badge variant={loan.status === "Approved" ? "default" : "secondary"} className="gap-1">
                      {loan.status === "Approved" ? <CheckCircle className="h-3 w-3" /> : <Clock className="h-3 w-3" />}
                      {loan.status}
                    </Badge>
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-muted-foreground">Loan Amount</p>
                      <p className="font-bold text-lg">{loan.amount}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Interest Rate</p>
                      <p className="font-medium">{loan.interestRate}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Purpose</p>
                      <p className="font-medium">{loan.purpose}</p>
                    </div>
                    <div>
                      <p className="text-muted-foreground">Term</p>
                      <p className="font-medium">{loan.term}</p>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Collateral: {loan.collateral}</p>
                  </div>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline">
                      View Details
                    </Button>
                    {loan.status === "Approved" && <Button size="sm">Accept Loan</Button>}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Valuation Process */}
          <Card>
            <CardHeader>
              <CardTitle>How Valuation Works</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium text-sm">AI Analysis</p>
                  <p className="text-xs text-muted-foreground">
                    Our AI analyzes your artwork's style, technique, and market demand
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium text-sm">Market Comparison</p>
                  <p className="text-xs text-muted-foreground">Compare with similar artworks sold in the market</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-primary text-primary-foreground rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium text-sm">Blockchain Record</p>
                  <p className="text-xs text-muted-foreground">Valuation is recorded on blockchain for transparency</p>
                </div>
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
                <DollarSign className="h-4 w-4" />
                Add New Artwork
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <FileText className="h-4 w-4" />
                Apply for Loan
              </Button>
              <Button variant="outline" className="w-full gap-2 bg-transparent">
                <TrendingUp className="h-4 w-4" />
                View Market Trends
              </Button>
            </CardContent>
          </Card>

          {/* Credit Score */}
          <Card>
            <CardHeader>
              <CardTitle>Credit Score</CardTitle>
              <CardDescription>Based on your art portfolio and loan history</CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold text-primary mb-2">785</div>
              <p className="text-sm font-medium mb-4">Excellent</p>
              <Progress value={78.5} className="mb-4" />
              <p className="text-xs text-muted-foreground">Your credit score qualifies you for premium loan rates</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
