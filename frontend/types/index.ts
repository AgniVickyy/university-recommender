export type StudentProfile = {
  name?: string;
  country_preference?: string;
  degree_level?: string;
  cgpa: number;
  backlogs?: number;
  ielts?: number;
  toefl?: number;
  duolingo?: number;
  det?: number;
  gre_quant?: number;
  gre_verbal?: number;
  work_experience?: number;
  research_papers?: number;
  budget: number;
  field?: string;
};

export type Recommendation = {
  id: number;
  name: string;
  country: string;
  degree: string;
  field: string;
  match_score: number;
  category: "Safe" | "Moderate" | "Ambitious";
  reason: string[];
  tuition_fee: number;
  ranking: number;
  acceptance_rate: number;
  explanation: string;
};

export type RecommendationResponse = {
  student_name?: string;
  total_matches: number;
  recommendations: Recommendation[];
};

export type University = {
  id: number;
  name: string;
  country: string;
  degree: string;
  field: string;
  min_cgpa: number;
  max_backlogs: number;
  min_det?: number;
  min_ielts?: number;
  min_toefl?: number;
  min_gre_quant?: number;
  min_gre_verbal?: number;
  tuition_fee: number;
  ranking: number;
  acceptance_rate: number;
};

export type UniversityDetail = University & {
  requirements: {
    min_cgpa: number;
    max_backlogs: number;
    min_det?: number;
    min_ielts?: number;
    min_toefl?: number;
    min_gre_quant?: number;
    min_gre_verbal?: number;
  };
  match_score?: number;
  category?: string;
  reason?: string[];
  explanation?: string;
  score_breakdown?: {
    cgpa_score: number;
    test_score: number;
    research_score: number;
    experience_score: number;
    budget_score: number;
  };
};

export type SortOption = "match_score" | "ranking" | "tuition" | "acceptance_rate";
