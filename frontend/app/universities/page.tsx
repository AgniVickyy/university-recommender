"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { getUniversities } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { University } from "@/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function UniversitiesPage() {
  const [universities, setUniversities] = useState<University[]>([]);
  const [search, setSearch] = useState("");
  const [country, setCountry] = useState("");
  const [degree, setDegree] = useState("");
  const [maxBudget, setMaxBudget] = useState("");
  const [maxRanking, setMaxRanking] = useState("");
  const [sortBy, setSortBy] = useState("ranking");

  useEffect(() => {
    getUniversities({
      search,
      country,
      degree,
      max_budget: maxBudget ? Number(maxBudget) : undefined,
      max_ranking: maxRanking ? Number(maxRanking) : undefined,
    })
      .then(setUniversities)
      .catch(() => setUniversities([]));
  }, [search, country, degree, maxBudget, maxRanking]);

  const sorted = useMemo(() => {
    const items = [...universities];
    items.sort((a, b) => {
      switch (sortBy) {
        case "tuition":
          return a.tuition_fee - b.tuition_fee;
        case "acceptance_rate":
          return a.acceptance_rate - b.acceptance_rate;
        default:
          return a.ranking - b.ranking;
      }
    });
    return items;
  }, [universities, sortBy]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Search Universities</h1>
        <p className="text-muted-foreground">Browse and filter the full university database.</p>
      </div>

      <div className="grid gap-3 rounded-xl border p-4 md:grid-cols-3 lg:grid-cols-6">
        <Input placeholder="Search name, country, program" value={search} onChange={(e) => setSearch(e.target.value)} />
        <Input placeholder="Country" value={country} onChange={(e) => setCountry(e.target.value)} />
        <Input placeholder="Degree (MS/PhD)" value={degree} onChange={(e) => setDegree(e.target.value)} />
        <Input placeholder="Max budget" value={maxBudget} onChange={(e) => setMaxBudget(e.target.value)} />
        <Input placeholder="Max ranking" value={maxRanking} onChange={(e) => setMaxRanking(e.target.value)} />
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger>
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ranking">Ranking</SelectItem>
            <SelectItem value="tuition">Tuition</SelectItem>
            <SelectItem value="acceptance_rate">Acceptance Rate</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {sorted.map((university) => (
          <Card key={university.id}>
            <CardHeader>
              <CardTitle className="text-xl">{university.name}</CardTitle>
              <p className="text-sm text-muted-foreground">
                {university.country} · {university.degree} · {university.field}
              </p>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="grid grid-cols-3 gap-2 text-sm">
                <div>
                  <p className="text-muted-foreground">Tuition</p>
                  <p>{formatCurrency(university.tuition_fee)}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Ranking</p>
                  <p>#{university.ranking}</p>
                </div>
                <div>
                  <p className="text-muted-foreground">Acceptance</p>
                  <p>{university.acceptance_rate}%</p>
                </div>
              </div>
              <Button asChild variant="outline" size="sm">
                <Link href={`/universities/${university.id}`}>View details</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
