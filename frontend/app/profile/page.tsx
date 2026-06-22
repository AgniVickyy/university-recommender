"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getRecommendations } from "@/lib/api";
import { PROFILE_STORAGE_KEY, RESULTS_STORAGE_KEY } from "@/lib/utils";
import { StudentProfile } from "@/types";

const defaultProfile: StudentProfile = {
  name: "",
  country_preference: "USA",
  degree_level: "MS",
  cgpa: 7.2,
  backlogs: 0,
  ielts: undefined,
  toefl: undefined,
  duolingo: 135,
  gre_quant: undefined,
  gre_verbal: undefined,
  work_experience: 0,
  research_papers: 0,
  budget: 40000,
  field: "Computer Engineering",
};

const steps = ["Academic Information", "Test Scores", "Preferences", "Review & Submit"];

export default function ProfilePage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState<StudentProfile>(defaultProfile);
  const [error, setError] = useState<string | null>(null);

  const progress = useMemo(() => ((step + 1) / steps.length) * 100, [step]);

  function updateField<K extends keyof StudentProfile>(key: K, value: StudentProfile[K]) {
    setProfile((current) => ({ ...current, [key]: value }));
  }

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const payload: StudentProfile = {
        ...profile,
        det: profile.duolingo ?? profile.det,
      };
      const results = await getRecommendations(payload);
      sessionStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(payload));
      sessionStorage.setItem(RESULTS_STORAGE_KEY, JSON.stringify(results));
      router.push("/results");
    } catch {
      setError("Failed to generate recommendations. Ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Student Profile</h1>
        <p className="text-muted-foreground">Multi-step form to capture your application profile.</p>
      </div>

      <div className="h-2 rounded-full bg-muted">
        <div className="h-2 rounded-full bg-primary transition-all" style={{ width: `${progress}%` }} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{steps[step]}</CardTitle>
          <CardDescription>Step {step + 1} of {steps.length}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {step === 0 && (
            <>
              <Field label="Full Name">
                <Input value={profile.name || ""} onChange={(e) => updateField("name", e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();

                      const form = e.currentTarget.form;
                      if (!form) return;

                      const index = Array.from(form.elements).indexOf(e.currentTarget);
                      const next = form.elements[index + 1] as HTMLElement;

                      next?.focus();
                    }
                  }}
                />
              </Field>
              <Field label="CGPA (10-point scale)">
                <Input
                  type="number"
                  step="0.1"
                  value={profile.cgpa === 0 ? "" : profile.cgpa}
                  onChange={(e) => updateField("cgpa", Number(e.target.value))}
                />
              </Field>
              <Field label="Backlogs">
                <Input
                  type="number"
                  value={profile.backlogs === 0 ? "" : profile.backlogs}
                  onChange={(e) => updateField("backlogs", Number(e.target.value))}
                />
              </Field>
              <Field label="Work Experience (Years)">
                <Input
                  type="number"
                  step="0.5"
                  placeholder="0"
                  value={profile.work_experience ?? ""}
                  onChange={(e) => updateField("work_experience", Number(e.target.value))}
                />
              </Field>
              <Field label="Research Publications">
                <Input
                  type="number"
                  placeholder="0"
                  value={profile.research_papers ?? ""}
                  onChange={(e) => updateField("research_papers", Number(e.target.value))}
                />
              </Field>
            </>
          )}

          {step === 1 && (
            <>
              <Field label="Duolingo / DET Score">
                <Input
                  type="number"
                  value={profile.duolingo === 0 ? "" : profile.duolingo}
                  onChange={(e) => updateField("duolingo", Number(e.target.value))}
                />
              </Field>
              <Field label="IELTS Score">
                <Input
                  type="number"
                  step="0.5"
                  value={profile.ielts === 0 ? "" : profile.ielts}
                  onChange={(e) => updateField("ielts", Number(e.target.value) || undefined)}
                />
              </Field>
              <Field label="TOEFL Score">
                <Input
                  type="number"
                  value={profile.toefl === 0 ? "" : profile.toefl}
                  onChange={(e) => updateField("toefl", Number(e.target.value) || undefined)}
                />
              </Field>
              <Field label="GRE Quant">
                <Input
                  type="number"
                  value={profile.gre_quant === 0 ? "" : profile.gre_quant}
                  onChange={(e) => updateField("gre_quant", Number(e.target.value) || undefined)}
                />
              </Field>
              <Field label="GRE Verbal">
                <Input
                  type="number"
                  value={profile.gre_verbal === 0 ? "" : profile.gre_verbal}
                  onChange={(e) => updateField("gre_verbal", Number(e.target.value) || undefined)}
                />
              </Field>
            </>
          )}

          {step === 2 && (
            <>
              <Field label="Country Preference">
                <Select
                  value={profile.country_preference}
                  onValueChange={(value) => updateField("country_preference", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select country" />
                  </SelectTrigger>
                  <SelectContent>
                    {["USA", "Canada", "UK", "Germany", "Australia", "Singapore"].map((country) => (
                      <SelectItem key={country} value={country}>
                        {country}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </Field>
              <Field label="Degree Level">
                <Select
                  value={profile.degree_level}
                  onValueChange={(value) => updateField("degree_level", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select degree" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="MS">MS</SelectItem>
                    <SelectItem value="PhD">PhD</SelectItem>
                  </SelectContent>
                </Select>
              </Field>
              <Field label="Preferred Field">
                <Input
                  value={profile.field || ""}
                  onChange={(e) => updateField("field", e.target.value)}
                />
              </Field>
              <Field label="Budget (USD)">
                <Input
                  type="number"
                  value={profile.budget}
                  onChange={(e) => updateField("budget", Number(e.target.value))}
                />
              </Field>
            </>
          )}

          {step === 3 && (
            <div className="grid gap-3 rounded-lg border p-4 text-sm md:grid-cols-2">
              {Object.entries(profile).map(([key, value]) => (
                <div key={key}>
                  <p className="text-muted-foreground">{key.replaceAll("_", " ")}</p>
                  <p className="font-medium">{String(value ?? "-")}</p>
                </div>
              ))}
            </div>
          )}

          {error && <p className="text-sm text-red-500">{error}</p>}

          <div className="flex justify-between pt-2">
            <Button variant="outline" disabled={step === 0} onClick={() => setStep((current) => current - 1)}>
              Back
            </Button>
            {step < steps.length - 1 ? (
              <Button onClick={() => setStep((current) => current + 1)}>Continue</Button>
            ) : (
              <Button onClick={handleSubmit} disabled={loading}>
                {loading ? "Generating..." : "Get Recommendations"}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      {children}
    </div>
  );
}
