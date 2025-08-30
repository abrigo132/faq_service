from sqlalchemy import select, ScalarResult, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Type
import logging

from sqlalchemy.orm import joinedload

from core.models import Question
from core.schemas import QuestionCreateRequest

logger = logging.getLogger(__name__)


class QuestionRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
        self.model: Type[Question] = Question

    async def add(self, question_creds: QuestionCreateRequest) -> Question:
        question = self.model(**question_creds.model_dump())
        try:
            self.session.add(question)
            await self.session.flush()
            return question
        except IntegrityError:
            logger.error(
                "Не удалось создать вопрос с текстом: %r",
                question_creds.text,
                exc_info=True,
            )
            await self.session.rollback()

    async def get(self) -> Sequence[Question]:
        stmt = select(self.model)
        questions: ScalarResult[Question] = await self.session.scalars(stmt)
        return questions.all()

    async def get_by_id(self, id: int) -> Question | None:
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(joinedload(self.model.answers))
        )
        question = await self.session.scalars(stmt)
        return question.unique().one_or_none()

    async def delete(self, id: int) -> Question | None:
        stmt = (
            select(Question)
            .where(Question.id == id)
            .options(joinedload(Question.answers))
        )
        result = await self.session.scalars(stmt)
        question = result.unique().one_or_none()

        if question:
            await self.session.delete(question)
            await self.session.flush()
            return question
        return question
