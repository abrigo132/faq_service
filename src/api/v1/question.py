from fastapi import APIRouter, Request

from core import settings
from core.services import QuestionService
from core.schemas import (
    QuestionAllResponse,
    QuestionCreateRequest,
    QuestionCreateResponse,
)

router = APIRouter(prefix=settings.api.v1.question, tags=["Question"])


@router.get("/", response_model=QuestionAllResponse)
async def get_all_question(request: Request):
    return await QuestionService().get_all_question()


@router.post("/", response_model=QuestionCreateResponse)
async def create_new_question(
    request: Request,
    question_creds: QuestionCreateRequest,
):
    return QuestionService().create_question(question_creds=question_creds)


@router.get("/{id}/")
async def get_question_by_id(
    request: Request,
    id: int,
):
    return QuestionService().get_question_with_answers(id=id)


@router.delete("/{id}/")
async def delete_question_by_id(
    request: Request,
    id: int,
):
    return QuestionService().delete_question_by_id(id=id)
