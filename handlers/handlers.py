from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.enums import ChatAction

from database.postgres import DB
from utils.messages import get_text, get_warn, get_error
from utils.decorators import rate_limit_commands, rate_limit_callbacks
from services import rate_limit
from utils.models import MODELS, get_model_display_name
from services.api_requests import openrouter
from utils.logger import logger
from keyboards import keyboards

router = Router()

# === Commands ===

@router.message(CommandStart())
@rate_limit_commands()
async def cmd_start(message: Message) -> None:
    await DB.add_user(message.from_user.id)
    text = get_text('start')
    await message.answer(text, parse_mode = ParseMode.HTML)

@router.message(Command('menu'))
@rate_limit_commands()
async def cmd_menu(message: Message) -> None:
    text = get_text('menu')
    await message.answer(text, reply_markup = keyboards.menu_keyboard(), parse_mode = ParseMode.HTML)

# === callbacks ===
@router.callback_query(F.data == 'help')
@rate_limit_callbacks()
async def callback_help(callback: CallbackQuery) -> None:
    text = get_text('help')
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'info')
@rate_limit_callbacks()
async def callback_info(callback: CallbackQuery) -> None:
    text = get_text('info')
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'faq')
@rate_limit_callbacks()
async def callback_faq(callback: CallbackQuery) -> None:
    text = get_text('faq')
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'models')
@rate_limit_callbacks()
async def callback_models(callback: CallbackQuery) -> None:
    text = get_text('models')
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'change_model')
@rate_limit_callbacks()
async def callback_change_model(callback: CallbackQuery) -> None:
    text = get_text('change_model')
    await callback.message.edit_text(text, reply_markup = keyboards.models_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('model_'))
@rate_limit_callbacks()
async def callback_new_model(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    model_alias = callback.data.split('_')[1]
    await DB.update_user_model(user_id, model_alias)
    model = get_model_display_name(model_alias)
    text = get_text('new_model', new_model = model)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'my_profile')
@rate_limit_callbacks()
async def callback_my_profile(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    user_record = await DB.get_user(user_id)
    current_model_alias = user_record['current_model']
    current_model = get_model_display_name(current_model_alias)
    created_at = user_record['created_at']
    created_str = created_at.strftime("%d.%m.%Y %H:%M")
    message_count = await DB.get_user_message_count(user_id)
    text = get_text('my_profile', id = user_id, current_model = current_model, message_count = message_count, created_str = created_str)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'statistics')
@rate_limit_callbacks()
async def callback_statistics(callback: CallbackQuery) -> None:
    statistics = await DB.get_global_stats()
    total_users = statistics['total_users']
    total_messages = statistics['total_messages']
    popular_model_alias = statistics['popular_model']
    popular_model = get_model_display_name(popular_model_alias)
    text = get_text('statistics', total_users = total_users, total_messages = total_messages, popular_model = popular_model)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'danger_zone')
@rate_limit_callbacks()
async def callback_danger_zone(callback: CallbackQuery) -> None:
    text = get_text('danger_zone')
    await callback.message.edit_text(text, reply_markup = keyboards.danger_zone_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'back_to_menu')
@rate_limit_callbacks()
async def callback_back_to_menu(callback: CallbackQuery) -> None:
    text = get_text('menu')
    await callback.message.edit_text(text, reply_markup = keyboards.menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('delete_'))
@rate_limit_callbacks()
async def callback_delete(callback: CallbackQuery) -> None:
    delete = callback.data.split('_')[1]
    try:
        if delete == 'messages':
            text = get_text('delete', delete = 'историю сообщений')
            await callback.message.edit_text(text, reply_markup = keyboards.delete_messages_keyboard(), parse_mode = ParseMode.HTML)
        else:
            text = get_text('delete', delete = 'историю сообщений и аккаунт')
            await callback.message.edit_text(text, reply_markup = keyboards.delete_account_keyboard(), parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

@router.callback_query(F.data.startswith('sure_'))
@rate_limit_callbacks()
async def callback_sure_delete(callback: CallbackQuery) -> None:
    delete = callback.data.split('_')[2]
    user_id = callback.from_user.id
    try:
        if delete == 'messages':
            await DB.delete_user_messages(user_id)
            text = get_text('mes_deleted')
            await callback.message.edit_text(text, parse_mode = ParseMode.HTML)
        else:
            await DB.delete_user(user_id)
            text = get_text('acc_deleted')
            await callback.message.edit_text(text, parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

# === text ===
@router.message(F.text)
async def handle_message(message: Message):
    if message.text.startswith('/'):
        return
    
    user_id = message.from_user.id
    
    remaining_time = await rate_limit.check_rate_limit(user_id)
    # Has it been 10 seconds since the previous request was answered?
    if remaining_time > 0:
        text = get_text('remaining_time', remaining_time = remaining_time)
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    # Checking if a request is already being processed
    if await rate_limit.check_processing_lock(user_id):
        text = get_text('request_processing')
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    try:
        await rate_limit.set_processing_lock(user_id)

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        user = await DB.get_user(user_id)
        if user == None:
            text = get_warn('not_registered')
            await message.answer(text, parse_mode = ParseMode.HTML)
            return
        model_alias = user['current_model'] # We get the model alias from the database
        model = MODELS[model_alias] # convert the alias to a real name

        context = await DB.get_user_recent_messages(user_id, model_alias) # Getting context (last 10 messages)

        response = await openrouter.generate_response(message.text, model, context)

        await DB.add_message(user_id, message.text, response, model_used=model_alias)
        await message.answer(response)

        await rate_limit.set_rate_limit(user_id)
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        text = get_error('error_in_handler')
        await message.answer(text)
    finally:
        await rate_limit.remove_processing_lock(user_id)

