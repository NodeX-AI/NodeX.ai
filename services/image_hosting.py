import aiohttp
import asyncio
import uuid
from typing import Optional
from config.config import *
from utils.logger import logger

async def upload(file_bytes: bytes) -> Optional[str]:
    url = IMAGE_HOSTING_URL
    
    data = aiohttp.FormData()
    data.add_field(
        'source',
        file_bytes,
        filename=f'{str(uuid.uuid4())}.jpg',
        content_type='image/jpeg'
    )
    data.add_field('key', IMAGE_HOSTING_KEY)
    data.add_field('action', 'upload')
    data.add_field('format', 'json')
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=data, timeout=60) as response: # 1 минута для хостинга изображения
                if response.status == 200:
                    result = await response.json()
                    if result.get('success'):
                        return result['image']['url']
                    else:
                        logger.error(f"[!] Ошибка freeimage.host: {result.get('error', 'Unknown error')}")
                        return None
                else:
                    error_text = await response.text()
                    logger.error(f"[!] Ошибка HTTP {response.status}: {error_text}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error("[!] Таймаут при загрузке на freeimage.host")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"[!] Ошибка сети при загрузке изображения: {e}")
            return None
        except Exception as e:
            logger.error(f"[!] Неожиданная ошибка при загрузке: {e}")
            return None