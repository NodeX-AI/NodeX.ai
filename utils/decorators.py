from functools import wraps
from aiogram.types import Message, CallbackQuery
from services.rate_limit import check_command_rate_limit, check_callback_rate_limit
from utils.messages import get_text
from aiogram.enums import ParseMode
import asyncio
from utils.tasks import delete_after_delay

# 1. The user types /start
# 2. wrapper(message) is called instead of cmd_start(message)

def rate_limit_commands(limit_seconds: int = 1):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            #3. Check the rate limit
            if not await check_command_rate_limit(message.from_user.id, limit_seconds):
                text = get_text('command_rate_limit')
                message = await message.answer(text, parse_mode = ParseMode.HTML)
                bot = message.bot
                chat_id = message.chat.id
                message_id = message.message_id
                asyncio.create_task(delete_after_delay(bot, chat_id, message_id))
                return
            # 4. If limit is OK, call the original function.
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator

def rate_limit_callbacks(limit_seconds: int = 1):
    def decorator(func):
        @wraps(func)
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            if not await check_callback_rate_limit(callback.from_user.id, limit_seconds):
                text = get_text('callback_rate_limit')
                message = await callback.message.answer(text, parse_mode = ParseMode.HTML)
                await callback.answer()
                bot = message.bot
                chat_id = message.chat.id
                message_id = message.message_id
                asyncio.create_task(delete_after_delay(bot, chat_id, message_id))
                return
            return await func(callback, *args, **kwargs)
        return wrapper
    return decorator