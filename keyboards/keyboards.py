from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def models_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Google: Gemma-3', callback_data = 'model_gemma')
    builder.button(text = 'DeepSeek R1T2 Chimera', callback_data = 'model_deepseek')
    builder.adjust(2)
    return builder.as_markup()