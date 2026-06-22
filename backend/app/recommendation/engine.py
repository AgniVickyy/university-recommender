from dataclasses import dataclass

from app.models.university import University
from app.schemas.student import StudentProfile


@dataclass
class RecommendationResult:
    match_score: float
    category: str
    reasons: list[str]
    cgpa_score: float
    test_score: float
    research_score: float
    experience_score: float
    budget_score: float


def _clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def _normalize_cgpa(cgpa: float) -> float:
    """Convert 10-point CGPA to 4.0 scale when needed."""
    if cgpa <= 4.0:
        return cgpa
    return round((cgpa / 10) * 4, 2)


def _calculate_cgpa_score(profile: StudentProfile, university: University) -> tuple[float, list[str]]:
    normalized_cgpa = _normalize_cgpa(profile.cgpa)
    reasons: list[str] = []
    if normalized_cgpa >= university.min_cgpa + 0.5:
        score = 25.0
        reasons.append("CGPA above requirement")
    elif normalized_cgpa >= university.min_cgpa:
        score = 20.0
        reasons.append("CGPA meets threshold")
    elif normalized_cgpa >= university.min_cgpa - 0.3:
        score = 12.0
        reasons.append("CGPA close to minimum requirement")
    else:
        score = 5.0
        reasons.append("CGPA below preferred threshold")

    if profile.backlogs <= university.max_backlogs:
        score += 5.0
        reasons.append("Backlogs within acceptable limit")
    else:
        score -= 5.0
        reasons.append("Backlogs exceed university limit")

    return _clamp(score), reasons


def _calculate_test_score(profile: StudentProfile, university: University) -> tuple[float, list[str]]:
    reasons: list[str] = []
    scores: list[float] = []

    if profile.det is not None and university.min_det is not None:
        if profile.det >= university.min_det + 10:
            scores.append(10.0)
            reasons.append("DET score exceeds minimum")
        elif profile.det >= university.min_det:
            scores.append(8.0)
            reasons.append("DET meets minimum requirement")
        else:
            scores.append(3.0)
            reasons.append("DET below minimum requirement")

    if profile.ielts is not None and university.min_ielts is not None:
        if profile.ielts >= university.min_ielts + 0.5:
            scores.append(8.0)
            reasons.append("IELTS above minimum")
        elif profile.ielts >= university.min_ielts:
            scores.append(6.0)
            reasons.append("IELTS meets minimum")
        else:
            scores.append(2.0)
            reasons.append("IELTS below minimum")

    if profile.toefl is not None and university.min_toefl is not None:
        if profile.toefl >= university.min_toefl + 10:
            scores.append(8.0)
            reasons.append("TOEFL above minimum")
        elif profile.toefl >= university.min_toefl:
            scores.append(6.0)
            reasons.append("TOEFL meets minimum")
        else:
            scores.append(2.0)
            reasons.append("TOEFL below minimum")

    if profile.gre_quant is not None and university.min_gre_quant is not None:
        if profile.gre_quant >= university.min_gre_quant + 5:
            scores.append(7.0)
            reasons.append("GRE Quant exceeds minimum")
        elif profile.gre_quant >= university.min_gre_quant:
            scores.append(5.0)
            reasons.append("GRE Quant meets minimum")
        else:
            scores.append(2.0)
            reasons.append("GRE Quant below minimum")

    if not scores:
        return 10.0, ["No test score requirements specified"]

    return _clamp(sum(scores), maximum=30.0), reasons


def _calculate_research_score(profile: StudentProfile) -> tuple[float, list[str]]:
    reasons: list[str] = []
    if profile.research_papers >= 3:
        score = 15.0
        reasons.append("Strong research profile")
    elif profile.research_papers >= 1:
        score = 10.0
        reasons.append("Research experience adds value")
    else:
        score = 5.0
        reasons.append("Limited research publications")
    return score, reasons


def _calculate_experience_score(profile: StudentProfile) -> tuple[float, list[str]]:
    reasons: list[str] = []
    if profile.work_experience >= 3:
        score = 15.0
        reasons.append("Strong professional experience")
    elif profile.work_experience >= 1:
        score = 10.0
        reasons.append("Relevant work experience")
    else:
        score = 5.0
        reasons.append("Limited work experience")
    return score, reasons


def _calculate_budget_score(profile: StudentProfile, university: University) -> tuple[float, list[str]]:
    reasons: list[str] = []
    if profile.budget >= university.tuition_fee + 10000:
        score = 15.0
        reasons.append("Budget sufficient with buffer")
    elif profile.budget >= university.tuition_fee:
        score = 12.0
        reasons.append("Budget sufficient")
    elif profile.budget >= university.tuition_fee * 0.85:
        score = 7.0
        reasons.append("Budget slightly below tuition")
    else:
        score = 3.0
        reasons.append("Budget below tuition requirement")
    return score, reasons


def _determine_category(match_score: float, profile: StudentProfile, university: University) -> str:
    cgpa_gap = _normalize_cgpa(profile.cgpa) - university.min_cgpa
    if match_score >= 80 and cgpa_gap >= 0.3:
        return "Safe"
    if match_score >= 65:
        return "Moderate"
    return "Ambitious"


def score_university(profile: StudentProfile, university: University) -> RecommendationResult:
    cgpa_score, cgpa_reasons = _calculate_cgpa_score(profile, university)
    test_score, test_reasons = _calculate_test_score(profile, university)
    research_score, research_reasons = _calculate_research_score(profile)
    experience_score, experience_reasons = _calculate_experience_score(profile)
    budget_score, budget_reasons = _calculate_budget_score(profile, university)

    match_score = _clamp(
        cgpa_score + test_score + research_score + experience_score + budget_score,
        maximum=100.0,
    )
    category = _determine_category(match_score, profile, university)
    reasons = cgpa_reasons + test_reasons + research_reasons + experience_reasons + budget_reasons

    return RecommendationResult(
        match_score=round(match_score, 1),
        category=category,
        reasons=reasons,
        cgpa_score=cgpa_score,
        test_score=test_score,
        research_score=research_score,
        experience_score=experience_score,
        budget_score=budget_score,
    )
