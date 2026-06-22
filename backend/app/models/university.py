from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class University(Base):
    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    degree: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    field: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    min_cgpa: Mapped[float] = mapped_column(Float, nullable=False)
    max_backlogs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    min_det: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_ielts: Mapped[float | None] = mapped_column(Float, nullable=True)
    min_toefl: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_gre_quant: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_gre_verbal: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tuition_fee: Mapped[int] = mapped_column(Integer, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    acceptance_rate: Mapped[float] = mapped_column(Float, nullable=False)
