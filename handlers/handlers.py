from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.enums import ChatAction
import asyncio

from database.postgres import DB
from utils.messages import get_text, get_error, get_prompt_all, get_prompt
from utils.md_cleaner import cleaner
from utils.decorators import rate_limit_commands, rate_limit_callbacks
from services import rate_limit
from utils.models import MODELS, get_model_display_name
from services.api_requests import openai
from utils.logger import logger
from keyboards import keyboards
from services.s3_storage import *

from aiogram.fsm.context import FSMContext
from utils.states import PromptStates

router = Router()

# === Commands ===

@router.message(CommandStart())
@rate_limit_commands()
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    await DB.add_user(user_id)
    lang = await DB.get_user_language(user_id)
    text = get_text('start', lang)
    await message.answer(text, parse_mode = ParseMode.HTML)

@router.message(Command('menu'))
@rate_limit_commands()
async def cmd_menu(message: Message) -> None:
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('menu', lang)
    await message.answer(text, reply_markup = keyboards.menu_keyboard(language = lang), parse_mode = ParseMode.HTML)

@router.message(Command('help'))
@rate_limit_commands()
async def cmd_help(message: Message) -> None:
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('help', lang)
    await message.answer(text, parse_mode = ParseMode.HTML)

@router.message(Command('support'))
@rate_limit_commands()
async def cmd_support(message: Message) -> None:
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('support', lang)
    await message.answer(text, reply_markup = keyboards.support_keyboard(language = lang), parse_mode = ParseMode.HTML)

# === callbacks ===

@router.callback_query(F.data == 'friends')
@rate_limit_callbacks()
async def callback_friends(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('friends', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.share_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()


@router.callback_query(F.data == 'info')
@rate_limit_callbacks()
async def callback_info(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('info', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'faq')
@rate_limit_callbacks()
async def callback_faq(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('faq', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'models')
@rate_limit_callbacks()
async def callback_models(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('models', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'prompt')
@rate_limit_callbacks()
async def callback_prompt(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('prompt', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.prompt_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('prompt_'))
@rate_limit_callbacks()
async def callback_prompt_actions(callback: CallbackQuery, state: FSMContext) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    action = callback.data.split('_')[1]
    try:
        if action == 'set':
            current_prompt = await DB.get_user_prompt(user_id)
            text = get_text('prompt_set', lang, prompt = current_prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.cancel_prompt_keyboard(language = lang), parse_mode = ParseMode.HTML)
            await state.set_state(PromptStates.waiting_for_prompt)
        elif action == 'reset':
            new_prompt = ''
            await DB.update_user_system_prompt(user_id, new_prompt)
            new_prompt = 'Не установлен' if lang == 'ru' else 'Not installed'
            text = get_text('new_prompt', lang, prompt = new_prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
        elif action == 'templates':
            text = get_text('prompt_templates', lang)
            await callback.message.edit_text(text, reply_markup = keyboards.prompt_templates_keyboard(language = lang), parse_mode = ParseMode.HTML)
        else: # guide
            text = get_text('prompt_guide', lang)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

@router.callback_query(F.data.startswith('template_'))
@rate_limit_callbacks()
async def callback_template_prompt(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    prompt_name = callback.data.split('_')[1]
    try:
        if prompt_name == 'exams':
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
        elif prompt_name == 'corrector':
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
        elif prompt_name == 'brainstorm':
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
        elif prompt_name == 'detail':
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
        elif prompt_name == 'laconic':
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
        else: #critical-thinking
            name, prompt, description = get_prompt_all(prompt_name, lang)
            text = get_text('prompt_template_message', lang, name = name, desc = description, text = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.set_template_keyboard(prompt_name, lang), parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

@router.callback_query(F.data.startswith('set_template_'))
@rate_limit_callbacks()
async def callback_set_template(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    template = callback.data.split('_')[2]
    try:
        if template == 'exams':
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
        elif template == 'corrector':
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
        elif template == 'brainstorm':
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
        elif template == 'detail':
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
        elif template == 'laconic':
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
        else: #critical-thinking
            prompt = get_prompt('text', template, lang)
            await DB.update_user_system_prompt(user_id, prompt)
            text = get_text('new_prompt', lang, prompt = prompt)
            await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
    finally:
        callback.answer()

@router.message(PromptStates.waiting_for_prompt)
async def process_new_prompt(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    message_len = len(message.text)
    if message_len > 600:
        text = get_text('long_prompt', lang, length = message_len)
        await message.answer(text, reply_markup = keyboards.cancel_prompt_keyboard(language = lang), parse_mode = ParseMode.HTML)
        return
    new_prompt = message.text.strip()
    await DB.update_user_system_prompt(user_id, new_prompt)
    text = get_text('new_prompt', language = lang, prompt = new_prompt)
    await message.answer(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await state.clear()

@router.callback_query(F.data == 'cancel_prompt')
@rate_limit_callbacks()
async def callback_cancel_prompt(callback: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == PromptStates.waiting_for_prompt:
        await state.clear()
        user_id = callback.from_user.id
        lang = await DB.get_user_language(user_id)
        text = get_text('cancel_prompt', lang)
        await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'back_to_templates')
@rate_limit_callbacks()
async def callback_back_to_templates(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('prompt_templates', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.prompt_templates_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'change_language')
@rate_limit_callbacks()
async def callback_change_language(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('change_language', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.change_language_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'change_image_model')
@rate_limit_callbacks()
async def callback_change_image_model(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('change_image_model', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.image_models_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'change_text_model')
@rate_limit_callbacks()
async def callback_change_text_model(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('change_model', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.text_models_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('language_'))
@rate_limit_callbacks()
async def callback_new_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    new_lang = callback.data.split('_')[1]
    await DB.update_user_language(user_id, new_lang)
    text = get_text('new_language', new_lang, lang = new_lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = new_lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('image_model_'))
@rate_limit_callbacks()
async def callback_new_image_model(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    model_alias = callback.data.split('_')[2]
    await DB.update_user_image_model(user_id, model_alias)
    model = get_model_display_name(model_alias)
    text = get_text('new_image_model', language = lang, new_model = model)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('text_model_'))
@rate_limit_callbacks()
async def callback_new_text_model(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    model_alias = callback.data.split('_')[2]
    await DB.update_user_text_model(user_id, model_alias)
    model = get_model_display_name(model_alias)
    text = get_text('new_model', lang, new_model = model)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'my_profile')
@rate_limit_callbacks()
async def callback_my_profile(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    user_record = await DB.get_user(user_id)
    current_model_alias = user_record['current_model']
    current_model = get_model_display_name(current_model_alias)
    current_image_model = get_model_display_name(user_record['image_model'])
    current_language = user_record['current_language']
    prompt = user_record['system_prompt']
    prompt = prompt if prompt else 'Не установлен' if current_language == 'ru' else 'Not installed'
    created_at = user_record['created_at']
    created_str = created_at.strftime("%d.%m.%Y %H:%M")
    message_count = await DB.get_user_message_count(user_id)
    text = get_text('my_profile', current_language, id = user_id, current_model = current_model, current_image_model = current_image_model, prompt = prompt, message_count = message_count, created_str = created_str, lang = current_language)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'statistics')
@rate_limit_callbacks()
async def callback_statistics(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    statistics = await DB.get_global_stats()
    total_users = statistics['total_users']
    total_messages = statistics['total_messages']
    popular_model_alias = statistics['popular_model']
    popular_model = get_model_display_name(popular_model_alias)
    text = get_text('statistics', lang, total_users = total_users, total_messages = total_messages, popular_model = popular_model)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'changelog')
@rate_limit_callbacks()
async def callback_changelog(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('changelog', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'danger_zone')
@rate_limit_callbacks()
async def callback_danger_zone(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('danger_zone', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.danger_zone_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'back_to_menu')
@rate_limit_callbacks()
async def callback_back_to_menu(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('menu', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.menu_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'back_to_support')
@rate_limit_callbacks()
async def callback_back_to_support(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('support', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.support_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'ideas')
@rate_limit_callbacks()
async def callback_ideas(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('ideas', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_support_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data == 'bug_report')
@rate_limit_callbacks()
async def callback_bug_report(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    text = get_text('bug_report', lang)
    await callback.message.edit_text(text, reply_markup = keyboards.back_to_support_keyboard(language = lang), parse_mode = ParseMode.HTML)
    await callback.answer()

@router.callback_query(F.data.startswith('delete_'))
@rate_limit_callbacks()
async def callback_delete(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    delete = callback.data.split('_')[1]
    try:
        if delete == 'messages':
            text = get_text('delete', lang, delete = '')
            await callback.message.edit_text(text, reply_markup = keyboards.delete_messages_keyboard(language = lang), parse_mode = ParseMode.HTML)
        else:
            delete = ' и аккаунт' if lang == 'ru' else ' and account'
            text = get_text('delete', lang, delete = delete)
            await callback.message.edit_text(text, reply_markup = keyboards.delete_account_keyboard(language = lang), parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

@router.callback_query(F.data.startswith('sure_'))
@rate_limit_callbacks()
async def callback_sure_delete(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    lang = await DB.get_user_language(user_id)
    delete = callback.data.split('_')[2]
    user_id = callback.from_user.id
    try:
        if delete == 'messages':
            await DB.delete_user_messages(user_id)
            text = get_text('mes_deleted', lang)
            await callback.message.edit_text(text, parse_mode = ParseMode.HTML)
        else:
            await DB.delete_user(user_id)
            text = get_text('acc_deleted', lang)
            await callback.message.edit_text(text, parse_mode = ParseMode.HTML)
    finally:
        await callback.answer()

# === text ===
@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    if message.text.startswith('/'):
        return
    
    
    remaining_time = await rate_limit.check_rate_limit(user_id)
    # Has it been 10 seconds since the previous request was answered?
    if remaining_time > 0:
        text = get_text('remaining_time', lang, remaining_time = remaining_time)
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    # Checking if a request is already being processed
    if await rate_limit.check_processing_lock(user_id):
        text = get_text('request_processing', lang)
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    try:
        await rate_limit.set_processing_lock(user_id)

        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        user = await DB.get_user(user_id)
        model_alias = user['current_model'] # We get the model alias from the database
        model = MODELS[model_alias] # convert the alias to a real name
        prompt = await DB.get_user_prompt(user_id)

        context = await DB.get_user_recent_messages(user_id, model_alias)
        response = await openai.generate_response(message.text, model, context, prompt)
        cleaned_response = cleaner.clean(response)
        await DB.add_message(user_id, message.text, cleaned_response, model_alias)
        
        if len(cleaned_response) > 4096:
            chunks = [cleaned_response[i:i+4096] for i in range(0, len(cleaned_response), 4096)]
            for chunk in chunks:
                await message.answer(chunk)
                await asyncio.sleep(1) # "умная отправка", если сообщение длинное = разбиваем его на куски и отправляем по частям
        else:
            await message.answer(cleaned_response)

        await rate_limit.set_rate_limit(user_id)
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        text = get_error('error_in_handler')
        await message.answer(text, parse_mode = ParseMode.HTML)
    finally:
        await rate_limit.remove_processing_lock(user_id)


@router.message(F.photo)
async def handle_image_message(message: Message):
    user_id = message.from_user.id
    lang = await DB.get_user_language(user_id)
    
    remaining_time = await rate_limit.check_rate_limit(user_id)
    if remaining_time > 0:
        text = get_text('remaining_time', lang, remaining_time = remaining_time)
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    if await rate_limit.check_processing_lock(user_id):
        text = get_text('request_processing', lang)
        await message.answer(text, parse_mode = ParseMode.HTML)
        return
    
    try:
        await rate_limit.set_processing_lock(user_id)
        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        user = await DB.get_user(user_id)
        model_alias = user['image_model']
        model = MODELS[model_alias]

        image = message.photo[-2] if len(message.photo) > 1 else message.photo[-1]
        file_id = image.file_id
        
        file = await message.bot.get_file(file_id)
        file_bytes_io = await message.bot.download_file(file.file_path)
        file_bytes = file_bytes_io.getvalue()

        image_url = await upload_to_s3(file_bytes)

        if not image_url:
            text = get_error('error_image_host')
            await message.answer(text, parse_mode=ParseMode.HTML)
            return
        
        mes = message.caption
        
        if not mes or mes.strip() == '':
            mes = 'Опиши изображение' if lang == 'ru' else 'Describe the image'
        
        message_with_image = f'{mes} {image_url}'
        context = await DB.get_user_recent_messages(user_id, model_alias, 2)
        prompt = await DB.get_user_prompt(user_id)
        response = await openai.generate_response_from_image(model, mes, image_url, context, prompt)
        cleaned_response = cleaner.clean(response)
        await DB.add_message(user_id, message_with_image, cleaned_response, model_alias)
        if len(cleaned_response) > 4096:
            chunks = [cleaned_response[i:i+4096] for i in range(0, len(cleaned_response), 4096)]
            for chunk in chunks:
                await message.answer(chunk)
                await asyncio.sleep(1) 
        else:
            await message.answer(cleaned_response)

        await rate_limit.set_rate_limit(user_id)
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        text = get_error('error_in_handler')
        await message.answer(text, parse_mode = ParseMode.HTML)
    finally:
        if image_url:
            try:
                await delete_from_s3(image_url)
            except Exception as delete_error:
                logger.error(f"[!] Не удалось удалить изображение: {delete_error}")
        await rate_limit.remove_processing_lock(user_id)
