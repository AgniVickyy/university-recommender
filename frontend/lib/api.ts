import {
  RecommendationResponse,
  StudentProfile,
  University,
  UniversityDetail,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export function getUniversities(params?: Record<string, string | number | undefined>) {
  const query = new URLSearchParams();
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== "") {
        query.set(key, String(value));
      }
    });
  }
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<University[]>(`/universities${suffix}`);
}

export function getRecommendations(profile: StudentProfile) {
  return request<RecommendationResponse>("/recommend", {
    method: "POST",
    body: JSON.stringify(profile),
  });
}

export function getUniversityDetail(id: number, profile?: Partial<StudentProfile>) {
  const query = new URLSearchParams();
  if (profile?.cgpa !== undefined) query.set("cgpa", String(profile.cgpa));
  if (profile?.budget !== undefined) query.set("budget", String(profile.budget));
  if (profile?.det !== undefined) query.set("det", String(profile.det));
  if (profile?.duolingo !== undefined) query.set("duolingo", String(profile.duolingo));
  if (profile?.backlogs !== undefined) query.set("backlogs", String(profile.backlogs));
  if (profile?.ielts !== undefined) query.set("ielts", String(profile.ielts));
  if (profile?.toefl !== undefined) query.set("toefl", String(profile.toefl));
  if (profile?.gre_quant !== undefined) query.set("gre_quant", String(profile.gre_quant));
  if (profile?.gre_verbal !== undefined) query.set("gre_verbal", String(profile.gre_verbal));
  if (profile?.work_experience !== undefined) {
    query.set("work_experience", String(profile.work_experience));
  }
  if (profile?.research_papers !== undefined) {
    query.set("research_papers", String(profile.research_papers));
  }

  const suffix = query.toString() ? `?${query.toString()}` : "";
  return request<UniversityDetail>(`/universities/${id}${suffix}`);
}
