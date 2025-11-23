import asyncio

async def delete_after_delay(bot, chat_id, message_id, delay = 3) -> None:
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        pass
