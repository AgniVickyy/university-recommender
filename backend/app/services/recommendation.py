from sqlalchemy.orm import Session

from app.models.university import University
from app.recommendation.engine import score_university
from app.schemas.student import RecommendationItem, RecommendationResponse, StudentProfile
from app.schemas.university import ScoreBreakdown, UniversityDetailResponse, UniversityRequirements
from app.services.explanation import generate_explanation


def _matches_filters(university: University, profile: StudentProfile) -> bool:
    if profile.country_preference and profile.country_preference.lower() not in university.country.lower():
        return False
    if profile.degree_level and profile.degree_level.upper() not in university.degree.upper():
        return False
    if profile.field and profile.field.lower() not in university.field.lower():
        return False
    return True


class RecommendationService:
    @staticmethod
    def recommend(db: Session, profile: StudentProfile) -> RecommendationResponse:
        universities = db.query(University).all()
        recommendations: list[RecommendationItem] = []

        for university in universities:
            if not _matches_filters(university, profile):
                continue

            result = score_university(profile, university)
            explanation = generate_explanation(profile, university, result)

            recommendations.append(
                RecommendationItem(
                    id=university.id,
                    name=university.name,
                    country=university.country,
                    degree=university.degree,
                    field=university.field,
                    match_score=int(round(result.match_score)),
                    category=result.category,
                    reason=result.reasons[:5],
                    tuition_fee=university.tuition_fee,
                    ranking=university.ranking,
                    acceptance_rate=university.acceptance_rate,
                    explanation=explanation,
                )
            )

        recommendations.sort(key=lambda item: item.match_score, reverse=True)

        return RecommendationResponse(
            student_name=profile.name,
            total_matches=len(recommendations),
            recommendations=recommendations,
        )

    @staticmethod
    def university_detail(
        db: Session,
        university_id: int,
        profile: StudentProfile | None = None,
    ) -> UniversityDetailResponse | None:
        university = db.query(University).filter(University.id == university_id).first()
        if not university:
            return None

        detail = UniversityDetailResponse(
            id=university.id,
            name=university.name,
            country=university.country,
            degree=university.degree,
            field=university.field,
            min_cgpa=university.min_cgpa,
            max_backlogs=university.max_backlogs,
            min_det=university.min_det,
            min_ielts=university.min_ielts,
            min_toefl=university.min_toefl,
            min_gre_quant=university.min_gre_quant,
            min_gre_verbal=university.min_gre_verbal,
            tuition_fee=university.tuition_fee,
            ranking=university.ranking,
            acceptance_rate=university.acceptance_rate,
            requirements=UniversityRequirements(
                min_cgpa=university.min_cgpa,
                max_backlogs=university.max_backlogs,
                min_det=university.min_det,
                min_ielts=university.min_ielts,
                min_toefl=university.min_toefl,
                min_gre_quant=university.min_gre_quant,
                min_gre_verbal=university.min_gre_verbal,
            ),
        )

        if profile:
            result = score_university(profile, university)
            detail.match_score = result.match_score
            detail.category = result.category
            detail.reason = result.reasons
            detail.explanation = generate_explanation(profile, university, result)
            detail.score_breakdown = ScoreBreakdown(
                cgpa_score=result.cgpa_score,
                test_score=result.test_score,
                research_score=result.research_score,
                experience_score=result.experience_score,
                budget_score=result.budget_score,
            )

        return detail
