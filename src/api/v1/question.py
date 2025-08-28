from fastapi import APIRouter, Request
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core import settings, db_helper
from core.services import QuestionService
from core.schemas import (
    QuestionAllResponse,
    QuestionCreateRequest,
    QuestionCreateResponse,
)

router = APIRouter(prefix=settings.api.v1.question, tags=["Question"])


@router.get("/", response_model=QuestionAllResponse)
async def get_all_question(
    request: Request,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await QuestionService(session=session).get_all_question()


@router.post("/", response_model=QuestionCreateResponse)
async def create_new_question(
    request: Request,
    question_creds: QuestionCreateRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await QuestionService(session=session).create_question(
        question_creds=question_creds
    )


@router.get("/{id}/")
async def get_question_by_id(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await QuestionService(session=session).get_question_with_answers(id=id)


@router.delete("/{id}/")
async def delete_question_by_id(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    return await QuestionService(session=session).delete_question_by_id(id=id)
