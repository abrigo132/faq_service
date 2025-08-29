from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from sqlalchemy import select

from core.models import Answer
from core.schemas import AnswerCreateRequest


class AnswerRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[Answer] = Answer

    async def add(self, answer_creds: AnswerCreateRequest) -> Answer:
        answer = self.model(**answer_creds.model_dump())
        self.session.add(answer)
        await self.session.flush()
        return answer

    async def get_by_id(self, answer_id: int) -> Answer | None:
        stmt = select(self.model).where(self.model.id == answer_id)
        result = await self.session.scalars(stmt)
        return result.one_or_none()

    async def delete(self, answer_id: int) -> Answer | None:
        stmt = select(self.model).where(self.model.id == answer_id)
        result = await self.session.scalars(stmt)
        answer = result.one_or_none()

        if answer:
            await self.session.delete(answer)
            await self.session.flush()
            return answer
        return answer
