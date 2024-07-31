from aioredis import Redis

from config import settings

redis = Redis.from_url(url=settings.redis_url)
