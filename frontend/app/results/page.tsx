"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { UniversityCard } from "@/components/university-card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { RESULTS_STORAGE_KEY } from "@/lib/utils";
import { Recommendation, RecommendationResponse, SortOption } from "@/types";

export default function ResultsPage() {
  const [data, setData] = useState<RecommendationResponse | null>(null);
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("all");
  const [category, setCategory] = useState("all");
  const [sortBy, setSortBy] = useState<SortOption>("match_score");

  useEffect(() => {
    const stored = sessionStorage.getItem(RESULTS_STORAGE_KEY);
    if (stored) {
      setData(JSON.parse(stored));
    }
  }, []);

  const filtered = useMemo(() => {
    if (!data) return [];

    let items = [...data.recommendations];

    if (search) {
      const query = search.toLowerCase();
      items = items.filter(
        (item) =>
          item.name.toLowerCase().includes(query) ||
          item.country.toLowerCase().includes(query) ||
          item.field.toLowerCase().includes(query),
      );
    }

    if (country !== "all") {
      items = items.filter((item) => item.country === country);
    }

    if (category !== "all") {
      items = items.filter((item) => item.category === category);
    }

    items.sort((a, b) => {
      switch (sortBy) {
        case "ranking":
          return a.ranking - b.ranking;
        case "tuition":
          return a.tuition_fee - b.tuition_fee;
        case "acceptance_rate":
          return a.acceptance_rate - b.acceptance_rate;
        default:
          return b.match_score - a.match_score;
      }
    });

    return items;
  }, [data, search, country, category, sortBy]);

  if (!data) {
    return (
      <div className="space-y-4">
        <h1 className="text-3xl font-bold">Results</h1>
        <p className="text-muted-foreground">No recommendations yet. Complete your profile first.</p>
        <Button asChild>
          <Link href="/profile">Go to Profile</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Your Recommendations</h1>
        <p className="text-muted-foreground">
          {data.total_matches} matches found
          {data.student_name ? ` for ${data.student_name}` : ""}.
        </p>
      </div>

      <div className="grid gap-3 rounded-xl border p-4 md:grid-cols-4">
        <Input
          placeholder="Search universities..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <Select value={country} onValueChange={setCountry}>
          <SelectTrigger>
            <SelectValue placeholder="Country" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Countries</SelectItem>
            {[...new Set(data.recommendations.map((item: Recommendation) => item.country))].map(
              (value) => (
                <SelectItem key={value} value={value}>
                  {value}
                </SelectItem>
              ),
            )}
          </SelectContent>
        </Select>
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger>
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="Safe">Safe</SelectItem>
            <SelectItem value="Moderate">Moderate</SelectItem>
            <SelectItem value="Ambitious">Ambitious</SelectItem>
          </SelectContent>
        </Select>
        <Select value={sortBy} onValueChange={(value) => setSortBy(value as SortOption)}>
          <SelectTrigger>
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="match_score">Match Score</SelectItem>
            <SelectItem value="ranking">Ranking</SelectItem>
            <SelectItem value="tuition">Tuition</SelectItem>
            <SelectItem value="acceptance_rate">Acceptance Rate</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {filtered.map((item) => (
          <UniversityCard key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}
