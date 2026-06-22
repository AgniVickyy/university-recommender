"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getUniversityDetail } from "@/lib/api";
import { formatCurrency, PROFILE_STORAGE_KEY } from "@/lib/utils";
import { StudentProfile, UniversityDetail } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function UniversityDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const [detail, setDetail] = useState<UniversityDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = sessionStorage.getItem(PROFILE_STORAGE_KEY);
    const profile: Partial<StudentProfile> | undefined = stored ? JSON.parse(stored) : undefined;

    getUniversityDetail(id, profile)
      .then(setDetail)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <p className="text-muted-foreground">Loading university details...</p>;
  }

  if (!detail) {
    return <p className="text-red-500">University not found.</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{detail.name}</h1>
        <p className="text-muted-foreground">
          {detail.country} · {detail.degree} · {detail.field}
        </p>
      </div>

      {detail.match_score !== undefined && (
        <Card>
          <CardHeader>
            <CardTitle>Your Match</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-3">
              <p className="text-4xl font-bold text-primary">{Math.round(detail.match_score)}%</p>
              {detail.category && <Badge>{detail.category}</Badge>}
            </div>
            {detail.explanation && <p className="text-sm text-muted-foreground">{detail.explanation}</p>}
            {detail.reason && (
              <ul className="space-y-1 text-sm">
                {detail.reason.map((item) => (
                  <li key={item}>✓ {item}</li>
                ))}
              </ul>
            )}
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>University Profile</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3 text-sm">
            <Stat label="Tuition" value={formatCurrency(detail.tuition_fee)} />
            <Stat label="Ranking" value={`#${detail.ranking}`} />
            <Stat label="Acceptance Rate" value={`${detail.acceptance_rate}%`} />
            <Stat label="Max Backlogs" value={String(detail.max_backlogs)} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Admission Requirements</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3 text-sm">
            <Stat label="Min CGPA (4.0 scale)" value={String(detail.requirements.min_cgpa)} />
            <Stat label="Min DET" value={String(detail.requirements.min_det ?? "N/A")} />
            <Stat label="Min IELTS" value={String(detail.requirements.min_ielts ?? "N/A")} />
            <Stat label="Min TOEFL" value={String(detail.requirements.min_toefl ?? "N/A")} />
            <Stat label="Min GRE Quant" value={String(detail.requirements.min_gre_quant ?? "N/A")} />
            <Stat label="Min GRE Verbal" value={String(detail.requirements.min_gre_verbal ?? "N/A")} />
          </CardContent>
        </Card>
      </div>

      {detail.score_breakdown && (
        <Card>
          <CardHeader>
            <CardTitle>Match Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-5">
            {Object.entries(detail.score_breakdown).map(([key, value]) => (
              <div key={key} className="rounded-lg border p-3">
                <p className="text-xs uppercase text-muted-foreground">{key.replace("_score", "")}</p>
                <p className="text-2xl font-semibold">{value}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-muted-foreground">{label}</p>
      <p className="font-medium">{value}</p>
    </div>
  );
}
