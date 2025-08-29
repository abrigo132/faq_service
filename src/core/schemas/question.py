from pydantic import BaseModel, field_validator
from datetime import datetime


class QuestionBase(BaseModel):
    text: str
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v):
        if not v.strip():
            raise ValueError(
                "Текст вопроса не может быть пустым или состоять только из пробелов"
            )
        return v


class QuestionAllResponse(QuestionBase):
    id: int


class QuestionListResponse(BaseModel):
    questions: list[QuestionAllResponse]


class QuestionCreateResponse(QuestionBase):
    id: int


class QuestionCreateRequest(QuestionBase):
    pass


class QuestionByIdWithAnswers(QuestionBase):
    id: int
    answers: list
