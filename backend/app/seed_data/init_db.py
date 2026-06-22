import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database.session import Base, engine
from app.seed_data.seed import seed_universities, SessionLocal


def init_db() -> None:
    db = SessionLocal()
    try:
        seed_universities(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized and seeded.")
