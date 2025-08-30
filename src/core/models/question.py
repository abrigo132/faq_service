from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import func, ForeignKey

from core.models import Base
from core.models.mixins import IdIntPkMixin


class Question(Base, IdIntPkMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    answers: Mapped[List["Answer"]] = relationship(
        "Answer", back_populates="question", cascade="all, delete"
    )


class Answer(Base, IdIntPkMixin):
    user_id: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey(column="questions.id"), nullable=False
    )

    question: Mapped["Question"] = relationship("Question", back_populates="answers")
