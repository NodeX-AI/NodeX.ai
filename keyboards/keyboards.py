from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def image_models_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Gemma 3', callback_data = 'image_model_gemma')
    builder.button(text = '⬅️ Назад в меню', callback_data = 'back_to_menu')
    builder.adjust(1)
    return builder.as_markup()

def text_models_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Gemma 3', callback_data = 'text_model_gemma')
    builder.button(text = 'DeepSeek R1T2 Chimera', callback_data = 'text_model_deepseek')
    builder.button(text = 'MiniMax M2', callback_data = 'text_model_minimax')
    builder.button(text = 'Nemotron Nano 9B V2', callback_data = 'text_model_nemotron')
    builder.button(text = '⬅️ Назад в меню', callback_data = 'back_to_menu')
    builder.adjust(2)
    return builder.as_markup()

def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = '⬅️ Назад в меню', callback_data = 'back_to_menu')
    builder.adjust(1)
    return builder.as_markup()

def danger_zone_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = '❌ Удалить историю сообщений', callback_data = 'delete_messages')
    builder.button(text = '❌ Удалить аккаунт', callback_data = 'delete_account')
    builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
    builder.adjust(1)
    return builder.as_markup()

def delete_messages_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Да, 100%', callback_data = 'sure_delete_messages')
    builder.button(text = 'Нет, я передумал', callback_data = 'back_to_menu')
    builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
    builder.adjust(1)
    return builder.as_markup()

def delete_account_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = 'Да, 100%', callback_data = 'sure_delete_account')
    builder.button(text = 'Нет, я передумал', callback_data = 'back_to_menu')
    builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
    builder.adjust(1)
    return builder.as_markup()

def menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text = '🤖 Доступные модели', callback_data = 'models')
    builder.button(text = '🔄 Изменить текстовую модель', callback_data = 'change_text_model')
    builder.button(text = '🔄 Изменить модель для распознавания изображений', callback_data = 'change_image_model')
    builder.button(text = '👤 Мой профиль', callback_data = 'my_profile')
    builder.button(text = '📊 Статистика', callback_data = 'statistics')
    builder.button(text = '⚠️ Опасная зона', callback_data = 'danger_zone')
    builder.button(text = '📕 Информация о проекте', callback_data = 'info')
    builder.button(text = '❓ ЧаВо', callback_data = 'faq')
    builder.adjust(2)
    return builder.as_markup()
