import aiohttp
import asyncio

from config.config import *
from utils.logger import logger
from utils.messages import get_error



class OpenAI_API_Service:
    def __init__(self):
        self.gpt5mini_key = GPT5_MINI_TOKEN
        self.gpt5mini_id = GPT5_MINI_ID
        self.gpt5mini_url = GPT5_MINI_BASE_URL
        self.gpt5mini_headers = {
            "content-type" : "application/json",
            "authorization" : f"Bearer {self.gpt5mini_key}",
        }

        self.grok4fast_key = GROK4_FAST_TOKEN
        self.grok4fast_id = GROK4_FAST_ID
        self.grok4fast_url = GROK4_FAST_BASE_URL
        self.grok4fast_headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.grok4fast_key}"
        }

        self.gemini3flashpreview_key = GEMINI_3_FLASH_PREVIEW_TOKEN
        self.gemini3flashpreview_id = GEMINI_3_FLASH_PREVIEW_ID
        self.gemini3flashpreview_url = GEMINI_3_FLASH_PREVIEW_URL
        self.gemini3flashpreview_headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.gemini3flashpreview_key}"
        }

        self.deepseekv32_key = DEEPSEEK_V3_TOKEN
        self.deepseekv32_id = DEEPSEEK_V3_ID
        self.deepseekv32_url = DEEPSEEK_V3_URL
        self.deepseekv32_headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.deepseekv32_key}"
        }

    def _get_text_model_config(self, model: str) -> dict:
        if 'grok' in model.lower():
            return {
                "base_url" : self.grok4fast_url + self.grok4fast_id + "/v1/chat/completions",
                "headers" : self.grok4fast_headers
            }
        elif "gpt-5" in model.lower():
            return {
                "base_url" : self.gpt5mini_url + self.gpt5mini_id + "/v1/chat/completions",
                "headers" : self.gpt5mini_headers
            }
        elif "deepseek" in model.lower():
            return {
                "base_url" : self.deepseekv32_url + self.deepseekv32_id + "/v1/chat/completions",
                "headers" : self.deepseekv32_headers
            }
        elif "gemini" in model.lower():
            return {
                "base_url" : self.gemini3flashpreview_url + self.gemini3flashpreview_id + "/v1/chat/completions",
                "headers" : self.gemini3flashpreview_headers
            }
    
    async def generate_response(self, message: str, model: str, context: list = None, prompt: str = '') -> str:
        model_config = self._get_text_model_config(model)
        messages = []
        messages.append({
            "role": "system",
            "content": prompt  
        })
        if context:
            reversed_context = context[::-1]
            for user_msg, ai_msg in reversed_context:
                messages.extend([
                {
                    "role": "user", 
                    "content": user_msg  
                },
                {
                    "role": "assistant", 
                    "content": ai_msg 
                }
            ])
        
        messages.append({
        "role": "user",
        "content": message  
        })

        payload = {
            "model" : model,
            "messages" : messages,
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
                logger.warning(f'[-] Таймаут: ({model})')
                error = get_error('timeout')
                return error
            except Exception as e:
                logger.error(f'[!] Непредвиденная ошибка: {e} | Модель: {model}')
                error = get_error('unexpected')
                return error
    async def generate_response_from_image(self, model: str, message: str, image_url: str, context, prompt: str = ''):
        model_config = self._get_text_model_config(model)
        messages = []
        messages.append({
            "role": "system",
            "content": prompt  
        })
        if context:
            reversed_context = context[::-1]
            for user_msg, ai_msg in reversed_context:
                messages.extend([
                    {
                    "role": "user", 
                    "content": user_msg  
                    },
                    {
                    "role": "assistant", 
                    "content": ai_msg 
                    }
                ])
        messages.append({
            "role": "user",
            "content" : [
                {
                    "type" : "text",
                    "text" : message
                },
                {
                    "type" : "image_url",
                    "image_url" : {"url" : image_url}
                }
            ],
        })
        payload = {
            "model" : model,
            "messages" : messages 
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
                logger.warning(f'[-] Таймаут: ({model})')
                error = get_error('timeout')
                return error
            except Exception as e:
                logger.error(f'[!] Непредвиденная ошибка: {e} | Модель: {model}')
                error = get_error('unexpected')
                return error

openai = OpenAI_API_Service()
