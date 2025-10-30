import asyncio
from aiogram import Bot, Dispatcher

from config import config
from handlers.handlers import router
from utils.logger import logger

from database.postgres import DB
from services.rate_limit import init_redis
from middleware.registration_middleware import RegistrationMiddleware
from middleware.error_logging_middleware import ErrorLoggingMiddleware

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher()

async def main():
    await DB.connect()
    logger.info('[*] Подключение к базе данных Postgres...')

    await init_redis()
    logger.info('[*] Подключение к Redis...')

    logger.info('[*] Подключение Middleware...')
    dp.update.outer_middleware(ErrorLoggingMiddleware())
    dp.callback_query.outer_middleware(ErrorLoggingMiddleware())
    dp.edited_message.outer_middleware(ErrorLoggingMiddleware())
    dp.message.outer_middleware(ErrorLoggingMiddleware())
    
    dp.message.middleware(RegistrationMiddleware())
    dp.callback_query.middleware(RegistrationMiddleware())

    logger.info('[*] Запуск бота...')
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())