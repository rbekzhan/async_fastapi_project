from redis.asyncio.connection import ConnectionPool
from app.core.config import settings
from redis.asyncio import Redis


class RedisService:
    def __init__(self):
        self._pool: ConnectionPool | None = None
        self.redis: Redis | None = None

    async def start(self):
        self._pool = ConnectionPool.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
        self.redis = Redis(connection_pool=self._pool, decode_responses=True)

    async def stop(self, exception: Exception = None):
        if self._pool:
            await self._pool.disconnect()
