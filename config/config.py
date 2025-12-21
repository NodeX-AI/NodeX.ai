import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_API_TOKEN')


PG_URL = os.getenv('PG_URL')
REDIS_URL = os.getenv('REDIS_URL')

IMAGE_HOSTING_KEY = os.getenv('IMAGE_HOSTING_KEY')
IMAGE_HOSTING_URL = os.getenv('IMAGE_HOSTING_URL')


GROK4_FAST_TOKEN = os.getenv('GROK4_FAST')
GPT5_MINI_TOKEN = os.getenv('GPT5MINI')

GROK4_FAST_ID = os.getenv('GROK4_FAST_ID')
GPT5_MINI_ID = os.getenv('GPT5_MINI_ID')

GEMMA3_IMAGES_TOKEN = os.getenv('GEMMA3_IMAGES')


GROK4_FAST_BASE_URL = os.getenv('GROK4_FAST_URL')
GPT5_MINI_BASE_URL = os.getenv('GPT5_MINI_URL')

AES_KEY = os.getenv('AES_KEY')