import time
from typing import Optional
import uuid
from config.config import *
from utils.logger import logger
import aioboto3
from config import *

S3_CONFIG = {
    'aws_access_key_id': S3_ACCESS_KEY,
    'aws_secret_access_key': S3_SECRET_KEY,
    'endpoint_url': S3_URL,
    'region_name': REGION_NAME
}

S3_BUCKET = BUCKET_NAME

async def upload_to_s3(file_bytes: bytes) -> Optional[str]:
    try:
        if hasattr(file_bytes, 'getvalue'):
            file_data = file_bytes.getvalue()
        else:
            file_data = file_bytes
        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}.jpg"
        
        async with aioboto3.Session().client('s3', **S3_CONFIG) as s3_client:
            await s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=unique_filename,
                Body=file_data,
                ContentType='image/jpeg',
                ACL='public-read'
            )
            public_url = f"https://{S3_BUCKET}.{S3_URL_DOMAIN}/{unique_filename}"
            
            logger.info(f"[*][S3] Файл загружен: {public_url}")
            return public_url
            
    except Exception as e:
        logger.error(f"[!][S3] Ошибка загрузки: {e}")
        return None


async def delete_from_s3(image_url: str) -> bool:
    try:
        if f"{S3_BUCKET}.s3.twcstorage.ru" in image_url:
            file_key = image_url.split(f"{S3_BUCKET}.{S3_URL_DOMAIN}/")[-1]
        elif S3_URL_DOMAIN in image_url:
            file_key = image_url.split(f"{S3_BUCKET}/")[-1]
        else:
            logger.error(f"[!][S3] Неизвестный формат ссылки: {image_url}")
            return False
        
        async with aioboto3.Session().client('s3', **S3_CONFIG) as s3_client:
            await s3_client.delete_object(
                Bucket=S3_BUCKET,
                Key=file_key
            )
            
            logger.info(f"[*][S3] Файл удален: {file_key}")
            return True
            
    except Exception as e:
        logger.error(f"[!][S3] Ошибка удаления: {e}")
        return False