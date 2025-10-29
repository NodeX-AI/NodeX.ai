from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def models_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Google: Gemma-3', callback_data = 'model_gemma')
    builder.button(text = 'DeepSeek R1T2 Chimera', callback_data = 'model_deepseek')
    builder.adjust(2)
    return builder.as_markup()

def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = '📚 Помощь', callback_data = 'help')
    builder.button(text = '🤖 Модели', callback_data = 'models')
    builder.button(text = '🔄 Изменить модель', callback_data = 'change_model')
    builder.button(text = '👤 Мой профиль', callback_data = 'my_profile')
    builder.button(text = '📊 Статистика', callback_data = 'statistics')
    builder.adjust(2)
    return builder.as_markup()