import redis.asyncio as redis

from config.config import REDIS_URL

redis_client = None

async def init_redis():
    global redis_client
    redis_client = await redis.from_url(REDIS_URL)

# ===

async def check_command_rate_limit(telegram_id: int, limit_seconds: int = 1) -> bool:
    key = f"command_rate_limit:{telegram_id}"
    current = await redis_client.get(key)
    
    if current is not None:
        return False
    
    await redis_client.setex(key, limit_seconds, 1)
    return True

# === 

async def check_rate_limit(telegram_id: int) -> int:
    key = f"rate_limit:{telegram_id}"
    
    ttl = await redis_client.ttl(key)
    
    if ttl == -2:
        return 0
    
    return max(0, ttl)

async def set_rate_limit(telegram_id: int, seconds: int = 10) -> None:
    key = f"rate_limit:{telegram_id}"
    await redis_client.setex(key, seconds, 1)

# ===

async def set_processing_lock(telegram_id: int, timeout: int = 120) -> None:
    key = f"processing:{telegram_id}"
    await redis_client.setex(key, timeout, 1)

async def check_processing_lock(telegram_id: int) -> bool:
    key = f"processing:{telegram_id}"
    return await redis_client.get(key) is not None

async def remove_processing_lock(telegram_id: int) -> None:
    key = f"processing:{telegram_id}"
    await redis_client.delete(key)
