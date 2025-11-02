import aiohttp
import asyncio

from config.config import *
from utils.logger import logger
from utils.messages import get_error

class OpenRouterService:
    def __init__(self):
        self.gemma3_key = GEMMA3_TOKEN
        self.deepseek_key = DEEPSEEK_TOKEN
        self.minimax_key = MINIMAX_TOKEN
        self.nemotron_key = NEMOTRON_TOKEN

        self.gemma3_base_url = GEMMA3_BASE_URL
        self.deepseek_base_url = DEEPSEEK_BASE_URL
        self.minimax_base_url = MINIMAX_M2_BASE_URL
        self.nemotron_base_url = NEMOTRON_BASE_URL

        self.headers_gemma3 = {
            'Authorization': f'Bearer {self.gemma3_key}',
            'Content-Type': 'application/json'
        }
        
        self.headers_deepseek = {
            'Authorization': f'Bearer {self.deepseek_key}',
            'Content-Type': 'application/json'
        }

        self.headers_minimax = {
            'Authorization': f'Bearer {self.minimax_key}',
            'Content-Type': 'application/json'
        }

        self.headers_nemotron = {
            'Authorization': f'Bearer {self.nemotron_key}',
            'Content-Type': 'application/json'
        }
    
    def _get_model_config(self, model: str) -> dict:
        if "gemma" in model.lower():
            return {
                "base_url": self.gemma3_base_url,
                "headers": self.headers_gemma3
            }
        elif "deepseek" in model.lower():
            return {
                "base_url": self.deepseek_base_url, 
                "headers": self.headers_deepseek
            }
        elif "minimax" in model.lower():
            return {
                "base_url": self.minimax_base_url,
                "headers": self.headers_minimax
            }
        elif "nemotron" in model.lower():
            return {
                "base_url": self.nemotron_base_url,
                "headers": self.headers_nemotron
            }
        else:
            return {
                "base_url": self.gemma3_base_url,
                "headers": self.headers_gemma3
            }
    
    async def generate_response(self, message: str, model: str, context: list = None) -> str:
        model_config = self._get_model_config(model)
        messages = []
        
        if context:
            for user_msg, ai_msg in context:
                messages.extend([
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": ai_msg}
                ])
        
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{model_config['base_url']}",
                    headers=model_config['headers'],
                    json=payload,
                    timeout=120
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        logger.error(f'[!] Ошибка API | Модель: {model} | Статус и ошибка: {response.status} - {error_text}')
                        error = get_error('api_err')
                        return error
                        
            except aiohttp.ClientError as e:
                logger.error(f'[!] Ошибка сети: ({model}): {e}')
                return f'❌ Ошибка сети'
            except asyncio.TimeoutError:
                logger.warning('[-] Таймаут: ({model})')
                error = get_error('timeout')
                return error
            except Exception as e:
                logger.error('[!] Непредвиденная ошибка: {e} | Модель: {model}')
                error = get_error('unexpected')
                return error

openrouter = OpenRouterService()
