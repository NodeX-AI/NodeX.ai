# Task: Check whether the user is registered before giving them access to manage and use the bot.
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from database.postgres import DB
from utils.messages import get_warn
from aiogram.enums import ParseMode


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message) and event.text and event.text.startswith('/start'):
            return await handler(event, data)
        user_id = event.from_user.id

        if not await DB.user_exists(user_id):
            text = get_warn('not_registered')
            if isinstance(event, Message):
                await event.answer(text)
            elif isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)
            return
        
        return await handler(event, data)