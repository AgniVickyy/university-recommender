"""Seed 50 sample universities into the database."""

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import SessionLocal
from app.models.university import University

UNIVERSITIES = [
    {"name": "Northeastern University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 5, "min_det": 120, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 56000, "ranking": 53, "acceptance_rate": 18.0},
    {"name": "Arizona State University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 8, "min_det": 105, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 32000, "ranking": 121, "acceptance_rate": 88.0},
    {"name": "North Carolina State University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 85, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 38000, "ranking": 58, "acceptance_rate": 47.0},
    {"name": "University of Southern California", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 125, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 62000, "ranking": 28, "acceptance_rate": 12.0},
    {"name": "Purdue University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 88, "min_gre_quant": 163, "min_gre_verbal": 152, "tuition_fee": 42000, "ranking": 43, "acceptance_rate": 53.0},
    {"name": "Texas A&M University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 160, "min_gre_verbal": 148, "tuition_fee": 35000, "ranking": 47, "acceptance_rate": 63.0},
    {"name": "University of Illinois Urbana-Champaign", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 48000, "ranking": 35, "acceptance_rate": 45.0},
    {"name": "Rutgers University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 83, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 39000, "ranking": 55, "acceptance_rate": 66.0},
    {"name": "Stony Brook University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 105, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 34000, "ranking": 58, "acceptance_rate": 48.0},
    {"name": "University of Florida", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 36000, "ranking": 28, "acceptance_rate": 31.0},
    {"name": "Georgia Institute of Technology", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 2, "min_det": 125, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 45000, "ranking": 33, "acceptance_rate": 17.0},
    {"name": "Carnegie Mellon University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.5, "max_backlogs": 2, "min_det": 130, "min_ielts": 7.0, "min_toefl": 100, "min_gre_quant": 167, "min_gre_verbal": 158, "tuition_fee": 58000, "ranking": 22, "acceptance_rate": 11.0},
    {"name": "University of Michigan", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 3, "min_det": 120, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 52000, "ranking": 21, "acceptance_rate": 20.0},
    {"name": "University of Washington", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 7.0, "min_toefl": 92, "min_gre_quant": 164, "min_gre_verbal": 154, "tuition_fee": 47000, "ranking": 40, "acceptance_rate": 48.0},
    {"name": "University of Texas at Austin", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 164, "min_gre_verbal": 152, "tuition_fee": 44000, "ranking": 32, "acceptance_rate": 32.0},
    {"name": "University of California San Diego", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 2, "min_det": 125, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 50000, "ranking": 28, "acceptance_rate": 24.0},
    {"name": "University of California Irvine", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 162, "min_gre_verbal": 150, "tuition_fee": 46000, "ranking": 33, "acceptance_rate": 29.0},
    {"name": "Ohio State University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 37000, "ranking": 43, "acceptance_rate": 68.0},
    {"name": "Virginia Tech", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 36000, "ranking": 47, "acceptance_rate": 57.0},
    {"name": "University of Maryland", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 96, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 43000, "ranking": 46, "acceptance_rate": 45.0},
    {"name": "University of Minnesota", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 38000, "ranking": 53, "acceptance_rate": 70.0},
    {"name": "University of Colorado Boulder", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 39000, "ranking": 97, "acceptance_rate": 81.0},
    {"name": "University of Utah", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 105, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 34000, "ranking": 115, "acceptance_rate": 89.0},
    {"name": "University of Arizona", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 7, "min_det": 105, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 33000, "ranking": 115, "acceptance_rate": 87.0},
    {"name": "University of South Florida", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 7, "min_det": 105, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 28000, "ranking": 124, "acceptance_rate": 43.0},
    {"name": "San Jose State University", "country": "USA", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 2.8, "max_backlogs": 10, "min_det": 100, "min_ielts": 6.0, "min_toefl": 75, "min_gre_quant": 150, "min_gre_verbal": 140, "tuition_fee": 26000, "ranking": 140, "acceptance_rate": 55.0},
    {"name": "University of Waterloo", "country": "Canada", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 7.0, "min_toefl": 90, "min_gre_quant": 163, "min_gre_verbal": 152, "tuition_fee": 30000, "ranking": 112, "acceptance_rate": 53.0},
    {"name": "University of Toronto", "country": "Canada", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 2, "min_det": 125, "min_ielts": 7.0, "min_toefl": 93, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 35000, "ranking": 21, "acceptance_rate": 43.0},
    {"name": "McGill University", "country": "Canada", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 6.5, "min_toefl": 86, "min_gre_quant": 162, "min_gre_verbal": 152, "tuition_fee": 32000, "ranking": 30, "acceptance_rate": 46.0},
    {"name": "University of British Columbia", "country": "Canada", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 163, "min_gre_verbal": 152, "tuition_fee": 33000, "ranking": 34, "acceptance_rate": 52.0},
    {"name": "Concordia University", "country": "Canada", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 2.8, "max_backlogs": 8, "min_det": 105, "min_ielts": 6.5, "min_toefl": 80, "min_gre_quant": 155, "min_gre_verbal": 145, "tuition_fee": 24000, "ranking": 150, "acceptance_rate": 78.0},
    {"name": "Imperial College London", "country": "UK", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.5, "max_backlogs": 2, "min_det": 130, "min_ielts": 7.0, "min_toefl": 100, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 45000, "ranking": 6, "acceptance_rate": 14.0},
    {"name": "University of Manchester", "country": "UK", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 32000, "ranking": 32, "acceptance_rate": 59.0},
    {"name": "University of Edinburgh", "country": "UK", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 6.5, "min_toefl": 92, "min_gre_quant": 162, "min_gre_verbal": 152, "tuition_fee": 34000, "ranking": 22, "acceptance_rate": 48.0},
    {"name": "University College London", "country": "UK", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 3, "min_det": 125, "min_ielts": 7.0, "min_toefl": 92, "min_gre_quant": 164, "min_gre_verbal": 154, "tuition_fee": 38000, "ranking": 9, "acceptance_rate": 63.0},
    {"name": "Technical University of Munich", "country": "Germany", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 88, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 8000, "ranking": 37, "acceptance_rate": 8.0},
    {"name": "RWTH Aachen University", "country": "Germany", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 88, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 6000, "ranking": 99, "acceptance_rate": 10.0},
    {"name": "TU Berlin", "country": "Germany", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 87, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 5000, "ranking": 154, "acceptance_rate": 8.0},
    {"name": "University of Melbourne", "country": "Australia", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 42000, "ranking": 14, "acceptance_rate": 70.0},
    {"name": "University of Sydney", "country": "Australia", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 85, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 43000, "ranking": 19, "acceptance_rate": 30.0},
    {"name": "Monash University", "country": "Australia", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 79, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 39000, "ranking": 42, "acceptance_rate": 40.0},
    {"name": "National University of Singapore", "country": "Singapore", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 2, "min_det": 125, "min_ielts": 6.5, "min_toefl": 92, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 38000, "ranking": 8, "acceptance_rate": 5.0},
    {"name": "Nanyang Technological University", "country": "Singapore", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 120, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 163, "min_gre_verbal": 152, "tuition_fee": 36000, "ranking": 15, "acceptance_rate": 7.0},
    {"name": "Delft University of Technology", "country": "Netherlands", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.2, "max_backlogs": 4, "min_det": 115, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 160, "min_gre_verbal": 150, "tuition_fee": 20000, "ranking": 47, "acceptance_rate": 55.0},
    {"name": "Eindhoven University of Technology", "country": "Netherlands", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 18000, "ranking": 136, "acceptance_rate": 57.0},
    {"name": "KTH Royal Institute of Technology", "country": "Sweden", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 16000, "ranking": 73, "acceptance_rate": 30.0},
    {"name": "University of Dublin Trinity College", "country": "Ireland", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.1, "max_backlogs": 5, "min_det": 110, "min_ielts": 6.5, "min_toefl": 88, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 25000, "ranking": 81, "acceptance_rate": 34.0},
    {"name": "University of Auckland", "country": "New Zealand", "degree": "MS", "field": "Computer Engineering", "min_cgpa": 3.0, "max_backlogs": 6, "min_det": 110, "min_ielts": 6.5, "min_toefl": 90, "min_gre_quant": 158, "min_gre_verbal": 148, "tuition_fee": 32000, "ranking": 68, "acceptance_rate": 45.0},
    {"name": "University of Massachusetts Amherst", "country": "USA", "degree": "PhD", "field": "Computer Engineering", "min_cgpa": 3.4, "max_backlogs": 2, "min_det": 120, "min_ielts": 7.0, "min_toefl": 92, "min_gre_quant": 165, "min_gre_verbal": 155, "tuition_fee": 42000, "ranking": 67, "acceptance_rate": 64.0},
    {"name": "University of Wisconsin Madison", "country": "USA", "degree": "PhD", "field": "Computer Engineering", "min_cgpa": 3.3, "max_backlogs": 3, "min_det": 115, "min_ielts": 6.5, "min_toefl": 92, "min_gre_quant": 163, "min_gre_verbal": 152, "tuition_fee": 40000, "ranking": 35, "acceptance_rate": 60.0},
]
def seed_universities(db: Session) -> None:
    try:
        existing = db.query(University).count()
    except Exception as e:
        print(f"Table not ready: {e}")
        return

    if existing:
        return

    for item in UNIVERSITIES:
        db.add(University(**item))

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed_universities(db)
        print(f"Seeded {len(UNIVERSITIES)} universities.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
