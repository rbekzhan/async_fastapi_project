from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi import status

from app.api.endpoints import router
from app.core.config import settings
from app.core.redis_connection import RedisService
from app.services.logger import setup_logger, logger
from fastapi.responses import JSONResponse


setup_logger(settings.log_level)

redis_instance = RedisService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_instance.start()
    app.state.redis = redis_instance.redis
    yield
    await redis_instance.stop()

app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)


@app.middleware("http")
async def logs_requests(request: Request, call_next):
    body = await request.body()
    logger.info(f"Request: {request.method} {request.url} - Body: {body.decode(errors='ignore')}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.middleware("http")
async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:

        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

app.include_router(router, prefix="/process_data")
