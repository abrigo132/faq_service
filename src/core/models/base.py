from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData

from core import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_convection)

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
