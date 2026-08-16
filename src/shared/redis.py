from redis.asyncio import Redis

from src.shared.config import settings

redis_client: Redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

# TODO: incomplete — the shared redis client is not wired into any service yet
