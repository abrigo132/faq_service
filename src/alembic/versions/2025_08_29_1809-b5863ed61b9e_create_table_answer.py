"""create table answer

Revision ID: b5863ed61b9e
Revises: b089848a529c
Create Date: 2025-08-29 18:09:23.466306

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b5863ed61b9e"
down_revision: Union[str, Sequence[str], None] = "b089848a529c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "answers",
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["questions.id"],
            name=op.f("fk_answers_question_id_questions"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_answers")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("answers")
