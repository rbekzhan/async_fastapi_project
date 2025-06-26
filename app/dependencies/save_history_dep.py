import json

from typing import Callable
from fastapi.routing import APIRoute
from fastapi import Request, Response
from redis.asyncio import Redis
from app.dependencies.redis_dep import get_redis
from app.services.redis_service import save_request_to_redis


class SaveHistoryRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            try:
                try:
                    input_data = await request.json()
                except Exception:
                    input_data = {}

                response = await original_route_handler(request)
                redis: Redis = get_redis(request)

                try:
                    await save_request_to_redis(
                        redis=redis,
                        method=request.method,
                        url=str(request.url),
                        input_data=input_data,
                        response_data=json.loads(response.body.decode()),
                        status_code=response.status_code
                    )
                except Exception as redis_exc:
                    print(f"Redis error: {redis_exc}")

                return response

            except Exception as e:
                redis: Redis = get_redis(request)
                try:
                    await save_request_to_redis(
                        redis=redis,
                        method=request.method,
                        url=str(request.url),
                        input_data=input_data,
                        response_data={"error": str(e)},
                        status_code=500
                    )
                except Exception as redis_exc:
                    print(f"Redis error in exception block: {redis_exc}")
                raise e

        return custom_handler
