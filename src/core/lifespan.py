from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

from core import db_helper, configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(level=logging.INFO)
    yield
    await db_helper.dispose()
