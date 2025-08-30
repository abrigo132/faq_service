from fastapi import HTTPException, status
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from repositories import QuestionRepository
from core.schemas import QuestionCreateRequest
from core.models import Question


logger = logging.getLogger(__name__)


class QuestionService:

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.question_repo = QuestionRepository(session=session)

    async def create_question(self, question_creds: QuestionCreateRequest) -> Question:
        logger.info("Создание вопроса с текстом: %r", question_creds.text)
        question: Question = await self.question_repo.add(question_creds=question_creds)
        await self.session.commit()
        return question

    async def get_all_question(self) -> Sequence[Question]:
        logger.info("Запрос на получение всех вопросов")
        questions = await self.question_repo.get()
        return questions

    async def delete_question_by_id(self, id: int):
        logger.info("Удаление вопроса с id %s", id)
        question = await self.question_repo.delete(id=id)
        if question is None:
            logger.error("Вопроса с id %s не существует", id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ответ с ID {id} не существует",
            )
        await self.session.commit()
        logger.info("Вопрос с id %s успешно удалён", id)
        return {"message": f"Ответ с ID {id} удален"}

    async def get_question_with_answers(self, id: int) -> Question | HTTPException:
        logger.info("Запрос вопроса с id %s", id)
        question: Question | None = await self.question_repo.get_by_id(id=id)
        if question is None:
            logger.error("Вопроса с id %s не существует", id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Вопрос с {id=} не найден",
            )

        return question
