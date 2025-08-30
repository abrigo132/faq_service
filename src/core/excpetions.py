from fastapi import HTTPException, status


class RepositoryException(HTTPException):
    """Базовое исключение для ошибок репозитория"""

    pass


class DuplicateEntryException(RepositoryException):
    """Исключение для дублирующихся записей"""

    def __init__(self, detail: str = "Запись уже существует"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ForeignKeyViolationException(RepositoryException):
    """Исключение для нарушений внешних ключей"""

    def __init__(self, detail: str = "Нарушение целостности внешнего ключа"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFoundException(RepositoryException):
    """Исключение для ненайденных записей"""

    def __init__(self, detail: str = "Запись не найдена"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
