import pytest
from unittest.mock import AsyncMock, patch
from core.services import QuestionService
from core.schemas import QuestionCreateRequest
from core.models import Question


@pytest.mark.asyncio
async def test_create_question():
    """Тест создания вопроса с использованием моков"""
    mock_session = AsyncMock()

    mock_question = Question(id=1, text="Тестовый вопрос")

    service = QuestionService(mock_session)

    with patch.object(
        service.question_repo, "add", AsyncMock(return_value=mock_question)
    ):
        question_data = QuestionCreateRequest(text="Тестовый вопрос")
        result = await service.create_question(question_data)

        assert result.id == 1
        assert result.text == "Тестовый вопрос"

        service.question_repo.add.assert_called_once()
        mock_session.commit.assert_called_once()
