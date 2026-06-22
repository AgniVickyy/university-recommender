"""Initial universities table

Revision ID: 001
Revises:
Create Date: 2026-06-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "universities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("degree", sa.String(length=20), nullable=False),
        sa.Column("field", sa.String(length=150), nullable=False),
        sa.Column("min_cgpa", sa.Float(), nullable=False),
        sa.Column("max_backlogs", sa.Integer(), nullable=False),
        sa.Column("min_det", sa.Integer(), nullable=True),
        sa.Column("min_ielts", sa.Float(), nullable=True),
        sa.Column("min_toefl", sa.Integer(), nullable=True),
        sa.Column("min_gre_quant", sa.Integer(), nullable=True),
        sa.Column("min_gre_verbal", sa.Integer(), nullable=True),
        sa.Column("tuition_fee", sa.Integer(), nullable=False),
        sa.Column("ranking", sa.Integer(), nullable=False),
        sa.Column("acceptance_rate", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_universities_country"), "universities", ["country"], unique=False)
    op.create_index(op.f("ix_universities_degree"), "universities", ["degree"], unique=False)
    op.create_index(op.f("ix_universities_field"), "universities", ["field"], unique=False)
    op.create_index(op.f("ix_universities_id"), "universities", ["id"], unique=False)
    op.create_index(op.f("ix_universities_name"), "universities", ["name"], unique=False)
    op.create_index(op.f("ix_universities_ranking"), "universities", ["ranking"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_universities_ranking"), table_name="universities")
    op.drop_index(op.f("ix_universities_name"), table_name="universities")
    op.drop_index(op.f("ix_universities_id"), table_name="universities")
    op.drop_index(op.f("ix_universities_field"), table_name="universities")
    op.drop_index(op.f("ix_universities_degree"), table_name="universities")
    op.drop_index(op.f("ix_universities_country"), table_name="universities")
    op.drop_table("universities")
