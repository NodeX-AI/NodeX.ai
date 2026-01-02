import asyncio
import time
from typing import Optional
import uuid
import aiohttp
from config.config import *
import random
import string
from utils.logger import logger

async def upload(file_bytes: bytes):
    try:
        url = RADIKAL_CLOUD_URL
        
        if hasattr(file_bytes, 'getvalue'):
            file_data = file_bytes.getvalue()
        else:
            file_data = file_bytes
        
        unique_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        form = aiohttp.FormData()
        form.add_field(
            name='source',
            value=file_data,
            filename=unique_filename,
            content_type='image/jpeg'
        )

        headers = {
            'X-API-Key': RADIKAL_CLOUD_KEY,
        }

        timeout = aiohttp.ClientTimeout(
            total=90,
            connect=15,
            sock_read=75
        )
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, data=form, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('status_code') == 200:
                        return result['image']['url'], result['image']['delete_url']
                    else:
                        error_msg = result.get('error', {}).get('message', 'Unknown error')
                        logger.error(f"[!] Ошибка API Radikal Cloud: {error_msg}")
                        return None, None
                else:
                    error_text = await response.text()
                    logger.error(f"[!] Ошибка HTTP: {response.status}: {error_text}")
                    return None, None
                    
    except asyncio.TimeoutError:
        logger.error(f"[!] Таймаут загрузки изображения")
        return None, None
    except aiohttp.ClientError as e:
        logger.error(f"[!] Ошибка сети: {e}")
        return None, None
    except Exception as e:
        logger.error(f"[!] Ошибка загрузки: {e}")
        return None, None
    
async def delete(delete_url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(delete_url) as response:
                if response.status == 200:
                    return True
                else:
                    return False
    except Exception as e:
        logger.error(f"[!] Ошибка при удалении: {e}")
        return False