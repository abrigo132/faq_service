from fastapi import APIRouter

from core import settings
from .question import router as question_router

router = APIRouter(prefix=settings.api.v1.prefix)
router.include_router(router=question_router)
