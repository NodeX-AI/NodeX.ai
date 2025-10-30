# middleware for logging errors in handlers
from utils.logger import logger
import traceback
from aiogram import BaseMiddleware
from aiogram.types import Update, Message, CallbackQuery
from aiogram.enums import ParseMode

from utils.messages import get_error


class ErrorLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        try:
            return await handler(event, data)
        except Exception as e:
            user_id = event.from_user.id if event.from_user else "Unknown"
            event_type = event.__class__.__name__
            
            logger.error(
                f"[!] Ошибка в {event_type} от пользователя {user_id}:\n"
                f"[!] - Ошибка: {e}\n"
                f"[!] - Трассировка: {traceback.format_exc()}"
            )
            
            if isinstance(event, (Message, CallbackQuery)):
                try:
                    text = get_error('error_in_handler')
                    if isinstance(event, Message):
                        await event.answer(text)
                    elif isinstance(event, CallbackQuery):
                        await event.answer(text, show_alert = True)
                except:
                    try:
                        await event.answer()
                    except:
                        pass
            return