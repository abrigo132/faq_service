import pytest
from unittest.mock import AsyncMock, patch

from core import NotFoundException
from core.services import AnswerService
from core.schemas import AnswerCreateRequest
from core.models import Answer, Question


@pytest.mark.asyncio
async def test_create_answer():
    """Тест создания ответа с использованием моков"""

    mock_session = AsyncMock()

    mock_answer = Answer(
        id=1, text="Тестовый ответ", user_id="test-user-uuid", question_id=1
    )

    mock_question = Question(id=1, text="Тестовый вопрос")

    service = AnswerService(mock_session)

    with patch.object(
        service.answer_repo, "add", AsyncMock(return_value=mock_answer)
    ), patch.object(
        service.question_repo, "get_by_id", AsyncMock(return_value=mock_question)
    ):
        answer_data = AnswerCreateRequest(
            text="Тестовый ответ", user_id="test-user-uuid", question_id=1
        )
        result = await service.create_answer(answer_data)

        assert result.id == 1
        assert result.text == "Тестовый ответ"
        assert result.user_id == "test-user-uuid"
        assert result.question_id == 1

        service.answer_repo.add.assert_called_once()
        service.question_repo.get_by_id.assert_called_once_with(id=1)
        mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_answer_nonexistent_question():
    """Тест создания ответа на несуществующий вопрос"""
    mock_session = AsyncMock()
    mock_question = None  # Вопрос не найден

    service = AnswerService(mock_session)

    # Мокируем получение вопроса - возвращаем None
    with patch.object(
        service.question_repo, "get_by_id", AsyncMock(return_value=mock_question)
    ):
        with pytest.raises(NotFoundException):
            answer_data = AnswerCreateRequest(
                text="Тестовый ответ",
                user_id="test-user-uuid",
                question_id=999,  # Несуществующий вопрос
            )
            await service.create_answer(answer_data)
