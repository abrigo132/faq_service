from fastapi import APIRouter, Request, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.schemas import AnswerCreateRequest, AnswerCreateResponse
from core.services import AnswerService

router = APIRouter(tags=["Answer"])


@router.post("/questions/{id}/answers/", response_model=AnswerCreateResponse)
async def create_answer(
    request: Request,
    answer_creds: AnswerCreateRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoints for create answer
    :param request:
    :param answer_creds: answer creds
    :param session: sqla async session
    :return:
    """
    return await AnswerService(session=session).create_answer(answer_creds=answer_creds)


@router.get("/answers/{id}/")
async def get_answer_by_id(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoints for get answer by id
    :param request:
    :param id: answer id
    :param session: sqla async session
    :return:
    """
    return await AnswerService(session=session).get_answer_by_id(answer_id=id)


@router.delete("/answers/{id}/")
async def delete_answer(
    request: Request,
    id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Endpoint for delete answer
    :param request:
    :param id: answer id
    :param session: sqla async session
    :return:
    """
    return await AnswerService(session=session).delete_answer(answer_id=id)
