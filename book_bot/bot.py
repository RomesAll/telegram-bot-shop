from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from book_bot.handlers import register_router
from config import settings

async def main():
    """Основаная функция запуска бота"""
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    register_router(dp)
    print('Бот запущен!')
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'Ошибка: {e}')
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())