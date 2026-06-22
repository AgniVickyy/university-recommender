import Link from "next/link";
import { ArrowRight, BrainCircuit, Filter, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="space-y-10">
      <section className="rounded-2xl border bg-gradient-to-br from-primary/10 via-background to-background p-8 md:p-12">
        <div className="max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border bg-background px-3 py-1 text-sm">
            <Sparkles className="h-4 w-4 text-primary" />
            Production-ready MVP
          </div>
          <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
            Find your best-fit universities with deterministic recommendations
          </h1>
          <p className="text-lg text-muted-foreground">
            Enter your academic profile, test scores, and budget to receive ranked university
            matches with Safe, Moderate, and Ambitious categories.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/profile">
                Start Profile <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/universities">Browse Universities</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <BrainCircuit className="mb-2 h-8 w-8 text-primary" />
            <CardTitle>Deterministic Engine</CardTitle>
            <CardDescription>
              Transparent scoring across CGPA, tests, research, experience, and budget.
            </CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <Filter className="mb-2 h-8 w-8 text-primary" />
            <CardTitle>Smart Filters</CardTitle>
            <CardDescription>
              Search and filter by country, budget, degree, and ranking with sorting controls.
            </CardDescription>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader>
            <Sparkles className="mb-2 h-8 w-8 text-primary" />
            <CardTitle>Rule-Based Insights</CardTitle>
            <CardDescription>
              Get human-readable explanations for every recommendation without external LLMs.
            </CardDescription>
          </CardHeader>
        </Card>
      </section>

      <Card>
        <CardHeader>
          <CardTitle>How it works</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-4">
          {[
            "Complete the 4-step student profile",
            "Submit to the recommendation API",
            "Review ranked university cards",
            "Explore detailed match breakdowns",
          ].map((step, index) => (
            <div key={step} className="rounded-lg border p-4">
              <p className="mb-2 text-sm font-semibold text-primary">Step {index + 1}</p>
              <p className="text-sm text-muted-foreground">{step}</p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
