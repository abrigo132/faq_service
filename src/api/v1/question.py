from fastapi import APIRouter, Request
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import logging

from core import settings, db_helper
from core.services import QuestionService
from core.schemas import (
    QuestionListResponse,
    QuestionCreateRequest,
    QuestionCreateResponse,
)

router = APIRouter(prefix=settings.api.v1.question, tags=["Question"])

logger = logging.getLogger(__name__)


@router.get("/", response_model=QuestionListResponse)
async def get_all_question(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoint for get all question
    :param request:
    :param session: sqla async session
    :return: QuestionListResponse
    """
    logger.info("Запрос на получение списка всех вопросов")
    questions = await QuestionService(session=session).get_all_question()
    logger.info("Успешно возвращено %d вопросов", len(questions))
    return {"questions": questions}


@router.post("/", response_model=QuestionCreateResponse)
async def create_new_question(
    request: Request,
    question_creds: QuestionCreateRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoint for create new question
    :param request:
    :param question_creds:
    :param session: sqla async session
    :return: QuestionCreateResponse
    """
    logger.info("Запрос на создание нового вопроса")
    logger.debug("Текст вопроса: %.100s...", question_creds.text)
    return await QuestionService(session=session).create_question(
        question_creds=question_creds
    )


@router.get("/{id}/")
async def get_question_by_id(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoint for get one question with answers
    :param request:
    :param id: question id
    :param session: sqla async session
    :return:
    """
    logger.info("Запрос на получение вопроса с ID: %d", id)
    return await QuestionService(session=session).get_question_with_answers(id=id)


@router.delete("/{id}/")
async def delete_question_by_id(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoint for delete question by id
    :param request:
    :param id: question id
    :param session: sqla async session
    :return:
    """
    logger.info("Запрос на удаление вопроса с ID: %d", id)
    return await QuestionService(session=session).delete_question_by_id(id=id)
