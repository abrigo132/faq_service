from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from uvicorn import run

from core import lifespan, settings
from api import router as api_router

app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(router=api_router)


if __name__ == "__main__":
    run(
        app=settings.app.app,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )
