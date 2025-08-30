from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type
from sqlalchemy import select
import logging

from core import DuplicateEntryException, ForeignKeyViolationException
from core.models import Answer
from core.schemas import AnswerCreateRequest


logger = logging.getLogger(__name__)


class AnswerRepository:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: Type[Answer] = Answer

    async def add(self, answer_creds: AnswerCreateRequest) -> Answer:
        try:
            answer = self.model(**answer_creds.model_dump())
            self.session.add(answer)
            await self.session.flush()
            return answer
        except IntegrityError as e:
            logger.error(
                "Не удалось создать вопрос с текстом: %r",
                answer_creds.text,
                exc_info=True,
            )
            await self.session.rollback()
            error_msg = str(e.orig)
            if "unique" in error_msg.lower():
                logger.error(
                    "Не удалось создать вопрос с текстом: %r - дубликат",
                    answer_creds.text,
                    exc_info=True,
                )
                raise DuplicateEntryException("Вопрос с таким текстом уже существует")
            else:
                logger.error(
                    "Не удалось создать вопрос с текстом: %r - ошибка целостности",
                    answer_creds.text,
                    exc_info=True,
                )
                raise ForeignKeyViolationException("Ошибка целостности данных")

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
