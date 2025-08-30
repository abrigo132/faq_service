import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000  # в миллисекундах
    formatted_process_time = f"{process_time:.2f}ms"

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {formatted_process_time}"
    )

    return response
