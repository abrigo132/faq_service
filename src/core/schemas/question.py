from pydantic import BaseModel
from datetime import datetime


class QuestionBase(BaseModel):
    text: str
    created_at: datetime


class QuestionAllResponse(QuestionBase):
    id: int


class QuestionCreateResponse(QuestionBase):
    id: int


class QuestionCreateRequest(QuestionBase):
    pass


class QuestionByIdWithAnswers(QuestionBase):
    id: int
    answers: list
