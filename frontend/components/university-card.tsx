import { Recommendation } from "@/types";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";

const categoryStyles: Record<string, string> = {
  Safe: "border-green-500/40 bg-green-500/10 text-green-700 dark:text-green-300",
  Moderate: "border-yellow-500/40 bg-yellow-500/10 text-yellow-700 dark:text-yellow-300",
  Ambitious: "border-red-500/40 bg-red-500/10 text-red-700 dark:text-red-300",
};

export function UniversityCard({ item }: { item: Recommendation }) {
  return (
    <Card className="transition hover:shadow-md">
      <CardHeader className="space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle className="text-xl">{item.name}</CardTitle>
            <p className="text-sm text-muted-foreground">
              {item.country} · {item.degree} · {item.field}
            </p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold text-primary">{item.match_score}%</p>
            <Badge className={categoryStyles[item.category]}>{item.category}</Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-3 gap-2 text-sm">
          <div>
            <p className="text-muted-foreground">Tuition</p>
            <p className="font-medium">{formatCurrency(item.tuition_fee)}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Ranking</p>
            <p className="font-medium">#{item.ranking}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Acceptance</p>
            <p className="font-medium">{item.acceptance_rate}%</p>
          </div>
        </div>
        <div>
          <p className="mb-2 text-sm font-medium">Reasons</p>
          <ul className="space-y-1 text-sm text-muted-foreground">
            {item.reason.slice(0, 3).map((reason) => (
              <li key={reason}>✓ {reason}</li>
            ))}
          </ul>
        </div>
        <Link href={`/universities/${item.id}`} className="text-sm font-medium text-primary hover:underline">
          View details →
        </Link>
      </CardContent>
    </Card>
  );
}
