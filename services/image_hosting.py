from typing import Optional
import aiohttp
from config.config import *
import random
import string
from utils.logger import logger


async def upload(file_bytes: bytes) -> Optional[str]:
    try:
        url = IMAGE_HOSTING_URL
        
        # ПРЕОБРАЗУЕМ BytesIO В bytes
        if hasattr(file_bytes, 'getvalue'):
            file_data = file_bytes.getvalue()  # если это BytesIO
        else:
            file_data = file_bytes  # если уже bytes
        
        boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        data = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="source"; filename="image.jpg"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        ).encode() + file_data + (  # ← ИСПОЛЬЗУЕМ file_data вместо file_bytes
            f'\r\n--{boundary}\r\n'
            f'Content-Disposition: form-data; name="key"\r\n\r\n{IMAGE_HOSTING_KEY}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="action"\r\n\r\nupload\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="format"\r\n\r\njson\r\n'
            f'--{boundary}--\r\n'
        ).encode()
        
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers, timeout=60) as response:
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
                    
    except Exception as e:
        logger.error(f"[!] Неожиданная ошибка при загрузке: {e}")
        return None