from pydantic import BaseModel, field_validator, Field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class QuestionBase(BaseModel):
    text: str = Field(
        min_length=1,
        description="Текст вопроса на вопрос не может быть пустым, или состоять из одних пробелов",
    )

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v):
        if not v.strip():
            logger.info("Ошибка валидации текста вопроса. Текст: %r", v)
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
