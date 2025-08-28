from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func

from core.models import Base
from core.models.mixins import IdIntPkMixin


class Question(Base, IdIntPkMixin):
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )
