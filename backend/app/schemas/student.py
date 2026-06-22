from pydantic import BaseModel, Field, model_validator


class StudentProfile(BaseModel):
    name: str | None = None
    country_preference: str | None = None
    degree_level: str | None = None
    cgpa: float = Field(..., ge=0, le=10)
    backlogs: int = Field(default=0, ge=0)
    ielts: float | None = Field(default=None, ge=0, le=9)
    toefl: int | None = Field(default=None, ge=0, le=120)
    duolingo: int | None = Field(default=None, ge=0, le=160)
    det: int | None = Field(default=None, ge=0, le=160)
    gre_quant: int | None = Field(default=None, ge=130, le=170)
    gre_verbal: int | None = Field(default=None, ge=130, le=170)
    work_experience: float = Field(default=0, ge=0)
    research_papers: int = Field(default=0, ge=0)
    budget: int = Field(..., ge=0)
    field: str | None = None

    @model_validator(mode="after")
    def sync_det_from_duolingo(self):
        if self.det is None and self.duolingo is not None:
            self.det = self.duolingo
        return self


class RecommendationItem(BaseModel):
    id: int
    name: str
    country: str
    degree: str
    field: str
    match_score: int
    category: str
    reason: list[str]
    tuition_fee: int
    ranking: int
    acceptance_rate: float
    explanation: str


class RecommendationResponse(BaseModel):
    student_name: str | None = None
    total_matches: int
    recommendations: list[RecommendationItem]
