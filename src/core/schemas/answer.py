from datetime import datetime
import logging

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class AnswerBase(BaseModel):
    """
    Answer Base pydantic model
    """

    question_id: int
    user_id: str
    text: str = Field(
        min_length=1,
        description="Текст ответа на вопрос не может быть пустым, или состоять из одних пробелов",
    )
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_text_not_empty(cls, v):
        if not v.strip():
            logger.info("Ошибка валидации текста вопроса. Текст: %r", v)
            raise ValueError(
                "Текст ответа не может быть пустым или состоять только из пробелов"
            )
        return v


class AnswerByIdRequest(AnswerBase):
    """
    Pydantic scheme for request answer by id
    """

    id: int


class AnswerCreateRequest(AnswerBase):
    """
    Pydantic scheme for create answer
    """

    pass


class AnswerCreateResponse(AnswerBase):
    id: int
