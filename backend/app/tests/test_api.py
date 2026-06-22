import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.session import Base, get_db
from app.main import app
from app.models.university import University
from app.recommendation.engine import score_university
from app.schemas.student import StudentProfile
from app.seed_data.seed import UNIVERSITIES


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    for item in UNIVERSITIES[:5]:
        session.add(University(**item))
    session.commit()
    yield session
    session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_universities(client):
    response = client.get("/universities")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_recommendation_engine_scores():
    university = University(**UNIVERSITIES[0])
    profile = StudentProfile(cgpa=7.2, det=135, budget=50000, backlogs=5)
    result = score_university(profile, university)
    assert 0 <= result.match_score <= 100
    assert result.category in {"Safe", "Moderate", "Ambitious"}
    assert result.reasons


def test_recommend_endpoint(client):
    payload = {
        "name": "Alex",
        "cgpa": 7.2,
        "det": 135,
        "budget": 50000,
        "backlogs": 5,
        "field": "Computer Engineering",
    }
    response = client.post("/recommend", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_matches"] >= 1
    assert data["recommendations"][0]["match_score"] >= 0


def test_university_detail(client):
    response = client.get(
        "/universities/1",
        params={"cgpa": 7.2, "det": 135, "budget": 50000},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Northeastern University"
    assert data["match_score"] is not None
