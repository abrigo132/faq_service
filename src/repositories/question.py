from sqlalchemy import select, ScalarResult, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Type

from core.models import Question
from core.schemas import QuestionCreateRequest


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
            await self.session.rollback()

    async def get(self) -> Sequence[Question]:
        stmt = select(self.model)
        questions: ScalarResult[Question] = await self.session.scalars(stmt)
        return questions.all()

    async def get_by_id(self, id: int) -> Question:
        pass

    async def delete(self, id: int):
        pass
