from app.models.university import University
from app.recommendation.engine import RecommendationResult, score_university
from app.schemas.student import StudentProfile


def generate_explanation(
    profile: StudentProfile,
    university: University,
    result: RecommendationResult,
) -> str:
    test_parts: list[str] = []
    if profile.det is not None:
        test_parts.append(f"DET {profile.det}")
    if profile.ielts is not None:
        test_parts.append(f"IELTS {profile.ielts}")
    if profile.toefl is not None:
        test_parts.append(f"TOEFL {profile.toefl}")
    if profile.gre_quant is not None:
        test_parts.append(f"GRE Quant {profile.gre_quant}")

    test_summary = ", ".join(test_parts) if test_parts else "your test profile"
    category_text = result.category.lower()

    cgpa_comment = (
        "Your CGPA exceeds the minimum requirement."
        if profile.cgpa >= university.min_cgpa + 0.3
        else "Your CGPA is close to the lower threshold."
        if profile.cgpa >= university.min_cgpa
        else "Your CGPA is below the typical requirement."
    )

    budget_comment = (
        "Your budget comfortably covers tuition."
        if profile.budget >= university.tuition_fee
        else "Your budget may require additional funding sources."
    )

    return (
        f"Based on your {profile.cgpa} CGPA and {test_summary}, "
        f"{university.name} is a {category_text} target. "
        f"{cgpa_comment} {budget_comment}"
    )
