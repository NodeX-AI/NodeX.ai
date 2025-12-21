from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def text_models_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Gemini 3 Flash Preview', callback_data = 'text_model_gemini3flashprev')
        builder.button(text = 'GPT-5 mini', callback_data = 'text_model_gpt5mini')
        builder.button(text = 'Grok 4 fast', callback_data = 'text_model_grok4fast')
        builder.button(text = 'DeepSeek V3.2', callback_data = 'text_model_deepseekv32')
        builder.button(text = '⬅️ Назад в меню', callback_data = 'back_to_menu')
        builder.adjust(2)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Gemini 3 Flash Preview', callback_data = 'text_model_gemini3flashprev')
        builder.button(text = 'GPT-5 mini', callback_data = 'text_model_gpt5mini')
        builder.button(text = 'Grok 4 fast', callback_data = 'text_model_grok4fast')
        builder.button(text = 'DeepSeek V3.2', callback_data = 'text_model_deepseekv32')
        builder.button(text = '⬅️ Back to menu', callback_data = 'back_to_menu')
        builder.adjust(2)
        return builder.as_markup()

def back_to_menu_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = '⬅️ Назад в меню', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = '⬅️ Back to menu', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()


def danger_zone_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = '❌ Удалить историю сообщений', callback_data = 'delete_messages')
        builder.button(text = '❌ Удалить аккаунт', callback_data = 'delete_account')
        builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = '❌ Delete message history', callback_data = 'delete_messages')
        builder.button(text = '❌ Delete account', callback_data = 'delete_account')
        builder.button(text = '⬅️ Back', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()


def delete_messages_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Да, 100%', callback_data = 'sure_delete_messages')
        builder.button(text = 'Нет, я передумал', callback_data = 'back_to_menu')
        builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Yes, 100%', callback_data = 'sure_delete_messages')
        builder.button(text = 'No, I changed my mind.', callback_data = 'back_to_menu')
        builder.button(text = '⬅️ Back', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()


def delete_account_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Да, 100%', callback_data = 'sure_delete_account')
        builder.button(text = 'Нет, я передумал', callback_data = 'back_to_menu')
        builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Yes, 100%', callback_data = 'sure_delete_account')
        builder.button(text = 'No, I changed my mind', callback_data = 'back_to_menu')
        builder.button(text = '⬅️ Back', callback_data = 'back_to_menu')
        builder.adjust(1)
        return builder.as_markup()


def menu_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = '🤖 Доступные модели', callback_data = 'models')
        builder.button(text = '📄 Изменить текстовую модель', callback_data = 'change_text_model')
        builder.button(text = '🔄 Сменить язык интерфейса', callback_data = 'change_language')
        builder.button(text = '👤 Мой профиль', callback_data = 'my_profile')
        builder.button(text = '📊 Статистика', callback_data = 'statistics')
        builder.button(text = '📑 Журнал изменений проекта', callback_data = 'changelog')
        builder.button(text = '⚠️ Опасная зона', callback_data = 'danger_zone')
        builder.button(text = '📕 Информация о проекте', callback_data = 'info')
        builder.button(text = '❓ ЧаВо', callback_data = 'faq')
        builder.adjust(2)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = '🤖 Available models', callback_data = 'models')
        builder.button(text = '📄 Change the text model', callback_data = 'change_text_model')
        builder.button(text = '🔄 Change interface language', callback_data = 'change_language')
        builder.button(text = '👤 My profile', callback_data = 'my_profile')
        builder.button(text = '📊 Statistics', callback_data = 'statistics')
        builder.button(text = '📑 Project change log', callback_data = 'changelog')
        builder.button(text = '⚠️ Danger zone', callback_data = 'danger_zone')
        builder.button(text = '📕 Project information', callback_data = 'info')
        builder.button(text = '❓ FaQ', callback_data = 'faq')
        builder.adjust(2)
        return builder.as_markup()

def change_language_keyboard(language: str = 'ru') -> InlineKeyboardMarkup:
    if language == 'ru':
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Русский 🇷🇺', callback_data = 'language_ru')
        builder.button(text = 'Английский 🇬🇧', callback_data = 'language_en')
        builder.button(text = '⬅️ Назад', callback_data = 'back_to_menu')
        builder.adjust(2)
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.button(text = 'Russian 🇷🇺', callback_data = 'language_ru')
        builder.button(text = 'English 🇬🇧', callback_data = 'language_en')
        builder.button(text = '⬅️ Back', callback_data = 'back_to_menu')
        builder.adjust(2)
        return builder.as_markup()
