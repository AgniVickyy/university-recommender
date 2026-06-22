from pydantic import BaseModel, ConfigDict, Field


class UniversityBase(BaseModel):
    name: str
    country: str
    degree: str
    field: str
    min_cgpa: float
    max_backlogs: int
    min_det: int | None = None
    min_ielts: float | None = None
    min_toefl: int | None = None
    min_gre_quant: int | None = None
    min_gre_verbal: int | None = None
    tuition_fee: int
    ranking: int
    acceptance_rate: float


class UniversityResponse(UniversityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UniversityRequirements(BaseModel):
    min_cgpa: float
    max_backlogs: int
    min_det: int | None = None
    min_ielts: float | None = None
    min_toefl: int | None = None
    min_gre_quant: int | None = None
    min_gre_verbal: int | None = None


class ScoreBreakdown(BaseModel):
    cgpa_score: float
    test_score: float
    research_score: float
    experience_score: float
    budget_score: float


class UniversityDetailResponse(UniversityResponse):
    requirements: UniversityRequirements
    match_score: float | None = None
    category: str | None = None
    reason: list[str] = Field(default_factory=list)
    explanation: str | None = None
    score_breakdown: ScoreBreakdown | None = None
