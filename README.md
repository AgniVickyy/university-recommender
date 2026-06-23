# University Recommendation Engine

A production-quality MVP that helps students find suitable universities based on academic profile and preferences. It includes a deterministic recommendation engine, FastAPI backend, PostgreSQL database, and a Next.js dashboard.

## Features

- Multi-step student profile form (Academic, Tests, Preferences, Review)
- Deterministic recommendation scoring (CGPA, tests, research, experience, budget)
- Safe / Moderate / Ambitious categorization
- Rule-based explanation generation (no external LLM)
- University search, filters, and sorting
- Dark mode, responsive UI with TailwindCSS and ShadCN-style components
- Docker Compose for local development
- Pytest coverage for API and recommendation engine

## Tech Stack

| Layer | Stack |
|-------|-------|
| Backend | Python, FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL |
| Frontend | Next.js 15, TypeScript, TailwindCSS |
| Deployment | Railway (backend + DB), Vercel (frontend) |

## Project Structure

```text
backend/
  app/
    api/              # FastAPI routes
    crud/             # Database queries
    database/         # SQLAlchemy session
    models/           # ORM models
    schemas/          # Pydantic schemas
    services/         # Business logic
    recommendation/   # Scoring engine
    seed_data/        # Seed scripts
    tests/            # Pytest tests
  alembic/            # Migrations

frontend/
  app/                # Next.js pages
  components/         # UI components
  lib/                # API client & utilities
  types/              # TypeScript types
```

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/university_recommendations
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
APP_ENV=development
```

### Frontend (`frontend/.env`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Local Development

### Option 1: Docker Compose (recommended)

```bash
cd "Tech Projects/university-recommendation-engineer"
docker-compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### Option 2: Manual setup

**Backend**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed_data.init_db
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/universities` | List/search universities |
| GET | `/universities/{id}` | University details + optional match |
| POST | `/recommend` | Generate ranked recommendations |

### Example Recommendation Request

```json
{
  "name": "Alex",
  "cgpa": 7.2,
  "det": 135,
  "budget": 50000,
  "backlogs": 5,
  "field": "Computer Engineering",
  "country_preference": "USA",
  "degree_level": "MS"
}
```

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest app/tests -v
```

## Railway Deployment (Backend + PostgreSQL)

1. Create a PostgreSQL service on Railway.
2. Deploy the `backend/` directory as a Python service.
3. Set environment variables:
   - `DATABASE_URL` (from Railway Postgres)
   - `CORS_ORIGINS` (your Vercel frontend URL)
4. Set start command:

```bash
python -m app.seed_data.init_db && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Vercel Deployment (Frontend)

1. Import the `frontend/` directory into Vercel.
2. Set `NEXT_PUBLIC_API_URL` to your Railway backend URL.
3. Deploy.

## Recommendation Scoring

For each university:

```python
score = cgpa_score + test_score + research_score + experience_score + budget_score
```

Categories:

- **Safe**: high match score with CGPA comfortably above minimum
- **Moderate**: solid match with some competitive factors
- **Ambitious**: lower match or profile near thresholds

CGPA on a 10-point scale is automatically normalized to a 4.0 scale.

## Seed Data

The database is seeded with 50 sample universities including:

- Northeastern University
- Arizona State University
- North Carolina State University
- University of Southern California
- Purdue University
- Texas A&M University
- UIUC
- Rutgers University
- Stony Brook University
- University of Florida

Run seed manually:

```bash
cd backend
python -m app.seed_data.seed
```

## License

MIT
