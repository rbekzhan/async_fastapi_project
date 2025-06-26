import json

from datetime import datetime
from uuid import uuid4
from typing import List
from redis.asyncio import Redis

REDIS_KEY_PREFIX = "request_history:"
TTL_SECONDS = 60 * 60 * 24 * 7  # 7 дней


async def save_request_to_redis(
    redis: Redis,
    method: str,
    url: str,
    input_data: dict,
    response_data: dict,
    status_code: int
) -> None:
    key = REDIS_KEY_PREFIX + str(uuid4())
    value = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "url": url,
        "input": input_data,
        "response": response_data,
        "status_code": status_code
    }
    await redis.set(key, json.dumps(value), ex=TTL_SECONDS)


async def get_last_n_requests(redis: Redis, n: int = 10) -> List[dict]:
    keys = await redis.keys(REDIS_KEY_PREFIX + "*")
    keys = sorted(keys, reverse=True)[0:n]
    results = await redis.mget(keys)
    return [json.loads(item) for item in results if item]
