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
    
    async def generate_response(self, message: str, model: str, context: list = None) -> str:
        model_config = self._get_text_model_config(model)
        messages = []
        if context:
            for user_msg, ai_msg in context:
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
    

class OpenRouterService:
    def __init__(self):
        self.gemma3_images_key = None

        self.gemma3_images_base_url = None

        self.heanders_gemma3_images = {
            'Authorization': f'Bearer {self.gemma3_images_key}',
            'Content-Type': 'application/json'
        }

    def _get_image_model_config(self, model: str) -> dict:
        if 'gemma' in model.lower():
            return {
                "base_url" : self.gemma3_images_base_url,
                "headers" : self.heanders_gemma3_images
            }
        
    async def generate_response(self, message: str, model: str, context: list = None) -> str:
        model_config = self._get_text_model_config(model)
        messages = []
        
        if context:
            for user_msg, ai_msg in context:
                messages.extend([
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": user_msg
                        }
                    ]
                },
                {
                    "role": "assistant", 
                    "content": [
                        {
                            "type": "text", 
                            "text": ai_msg
                        }
                    ]
                    }
                ])
        
        messages.append({
        "role": "user", 
        "content": [
            {
                "type": "text",
                "text": message
            }
            ]
        })
        
        payload = {
            "model": model,
            "messages": messages,
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
            
    async def generate_response_from_image(self, url: str, model: str, prompt: str) -> str:
        model_config = self._get_image_model_config(model)
        
        messages = [{
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            ]
        }]

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
                logger.warning(f'[-] Таймаут: ({model})')
                error = get_error('timeout')
                return error
            except Exception as e:
                logger.error(f'[!] Непредвиденная ошибка: {e} | Модель: {model}')
                error = get_error('unexpected')
                return error

openrouter = OpenRouterService()
openai = OpenAI_API_Service()