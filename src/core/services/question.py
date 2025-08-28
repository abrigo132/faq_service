from fastapi import Depends
from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import QuestionRepository
from core import db_helper
from core.schemas import QuestionCreateRequest
from core.models import Question


class QuestionService:

    def __init__(self, session: AsyncSession = Depends(db_helper.session_getter)):
        self.session: AsyncSession = session
        self.question_repo = QuestionRepository(session=session)

    async def create_question(self, question_creds: QuestionCreateRequest) -> Question:
        question: Question = await self.question_repo.add(question_creds=question_creds)
        await self.session.commit()
        return question

    async def get_all_question(self) -> Sequence[Question]:
        questions = await self.question_repo.get()
        return questions

    async def delete_question_by_id(self, id: int):
        pass

    async def get_question_with_answers(self, id: int):
        pass
