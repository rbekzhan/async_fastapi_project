from typing import Any, Dict
from fastapi import APIRouter, Request, Depends, Body
from redis.asyncio import Redis
from datetime import datetime
from uuid import uuid4
from app.dependencies.save_history_dep import SaveHistoryRoute
from app.dependencies.redis_dep import get_redis
from app.models.schemas import ProcessDataResponse
from app.services.external_api import fetch_cat_fact
from app.services.redis_service import get_last_n_requests

router = APIRouter(route_class=SaveHistoryRoute)

@router.post("/", response_model=ProcessDataResponse)
async def process_data(
    request: Request,
    input_json: Dict[str, str] = Body(
        ...,
        example={
            "name": "Behan"
        }
    ),
    redis: Redis = Depends(get_redis)
):
    processed_data = {
        "processed_at": datetime.utcnow().isoformat(),
        "request_id": str(uuid4())
    }
    cat_fact = await fetch_cat_fact()

    return {
        "processed_data": processed_data | input_json,
        "cat_fact": cat_fact
    }


@router.get("/history/")
async def get_history(
    redis: Redis = Depends(get_redis),
    n: int = 10
):
    return await get_last_n_requests(redis, n)
