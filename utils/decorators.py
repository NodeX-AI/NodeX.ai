from functools import wraps
from aiogram.types import Message, CallbackQuery
from services.rate_limit import check_command_rate_limit, check_callback_rate_limit
from utils.messages import get_text
from aiogram.enums import ParseMode

# 1. The user types /start
# 2. wrapper(message) is called instead of cmd_start(message)

def rate_limit_commands(limit_seconds: int = 1):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            #3. Check the rate limit
            if not await check_command_rate_limit(message.from_user.id, limit_seconds):
                text = get_text('command_rate_limit')
                await message.answer(text, parse_mode = ParseMode.HTML)
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
                await callback.message.answer(text, parse_mode = ParseMode.HTML)
                return
            return await func(callback, *args, **kwargs)
        return wrapper
    return decorator