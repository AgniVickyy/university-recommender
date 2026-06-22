from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.university import get_universities, get_university
from app.database.session import get_db
from app.schemas.student import RecommendationResponse, StudentProfile
from app.schemas.university import UniversityResponse
from app.services.recommendation import RecommendationService

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/universities", response_model=list[UniversityResponse])
def list_universities(
    search: str | None = Query(default=None),
    country: str | None = Query(default=None),
    degree: str | None = Query(default=None),
    max_budget: int | None = Query(default=None),
    max_ranking: int | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[UniversityResponse]:
    return get_universities(
        db,
        search=search,
        country=country,
        degree=degree,
        max_budget=max_budget,
        max_ranking=max_ranking,
    )


@router.get("/universities/{university_id}")
def university_details(
    university_id: int,
    cgpa: float | None = Query(default=None),
    backlogs: int | None = Query(default=0),
    det: int | None = Query(default=None),
    duolingo: int | None = Query(default=None),
    ielts: float | None = Query(default=None),
    toefl: int | None = Query(default=None),
    gre_quant: int | None = Query(default=None),
    gre_verbal: int | None = Query(default=None),
    work_experience: float | None = Query(default=0),
    research_papers: int | None = Query(default=0),
    budget: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    profile = None
    if cgpa is not None and budget is not None:
        profile = StudentProfile(
            cgpa=cgpa,
            backlogs=backlogs or 0,
            det=det,
            duolingo=duolingo,
            ielts=ielts,
            toefl=toefl,
            gre_quant=gre_quant,
            gre_verbal=gre_verbal,
            work_experience=work_experience or 0,
            research_papers=research_papers or 0,
            budget=budget,
        )

    detail = RecommendationService.university_detail(db, university_id, profile)
    if not detail:
        raise HTTPException(status_code=404, detail="University not found")
    return detail


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(
    profile: StudentProfile,
    db: Session = Depends(get_db),
) -> RecommendationResponse:
    return RecommendationService.recommend(db, profile)
