import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_API_TOKEN')


PG_URL = os.getenv('PG_URL')
REDIS_URL = os.getenv('REDIS_URL')


GEMMA3_TOKEN = os.getenv('GEMMA3')
DEEPSEEK_TOKEN = os.getenv('DEEPSEEK')


GEMMA3_BASE_URL = os.getenv('GEMMA3_BASE_URL')
DEEPSEEK_BASE_URL = os.getenv('DEEPSEEK_R1T2_CHIMERA_BASE_URL')