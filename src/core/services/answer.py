from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from fastapi import status
import logging

from core.models import Answer
from repositories import AnswerRepository, QuestionRepository
from core.schemas import AnswerCreateRequest

logger = logging.getLogger(__name__)


class AnswerService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.answer_repo = AnswerRepository(session=session)
        self.question_repo = QuestionRepository(session=session)

    async def create_answer(self, answer_creds: AnswerCreateRequest) -> Answer:
        question = await self.question_repo.get_by_id(id=answer_creds.question_id)
        if question is None:
            logger.info("Вопрос с id %s не найден", answer_creds.question_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вопрос с ID {answer_creds.question_id} не существует",
            )

        answer: Answer = await self.answer_repo.add(answer_creds=answer_creds)
        await self.session.commit()
        logger.info(
            "Ответ на вопрос с id %s с текстом %r успешно создан",
            (answer_creds.question_id, answer_creds.text),
        )
        return answer

    async def get_answer_by_id(self, answer_id: int) -> Answer:
        answer: Answer = await self.answer_repo.get_by_id(answer_id=answer_id)
        if answer is None:
            logger.info("Ответ с id %s не найден", answer_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ответ с ID {answer_id} не существует",
            )
        logger.info("Ответ с id %s найден", answer_id)
        return answer

    async def delete_answer(self, answer_id: int):
        answer = await self.answer_repo.delete(answer_id=answer_id)
        if answer is None:
            logger.info("Ответ с id %s не найден для удаления", answer_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ответ с ID {answer_id} не существует",
            )
        await self.session.commit()
        logger.info("Ответ с id %s удалён", answer_id)
        return {"message": f"Ответ с ID {answer_id} удален"}
