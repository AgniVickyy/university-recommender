from sqlalchemy.orm import Session

from app.models.university import University


def get_universities(
    db: Session,
    *,
    search: str | None = None,
    country: str | None = None,
    degree: str | None = None,
    max_budget: int | None = None,
    max_ranking: int | None = None,
) -> list[University]:
    query = db.query(University)

    if search:
        pattern = f"%{search.lower()}%"
        query = query.filter(
            (University.name.ilike(pattern))
            | (University.country.ilike(pattern))
            | (University.field.ilike(pattern))
        )
    if country:
        query = query.filter(University.country.ilike(f"%{country}%"))
    if degree:
        query = query.filter(University.degree.ilike(f"%{degree}%"))
    if max_budget is not None:
        query = query.filter(University.tuition_fee <= max_budget)
    if max_ranking is not None:
        query = query.filter(University.ranking <= max_ranking)

    return query.order_by(University.ranking.asc()).all()


def get_university(db: Session, university_id: int) -> University | None:
    return db.query(University).filter(University.id == university_id).first()
