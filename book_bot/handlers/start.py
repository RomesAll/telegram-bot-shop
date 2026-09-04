from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from book_bot.handlers.book_reader import show_library
from book_bot.handlers.catalog import show_catalog
from book_bot.keyboards.reply import get_start_keyboard
from book_bot.keyboards.inline import get_main_menu
from book_bot.config import settings

router = Router()

@router.message(Command("start"))
async def boot_start(message: Message):
    """Обработка команды /start"""
    welcome_text = (
        "<b>Добро пожаловать в BookBot!</b>\n\n"
        "📚 Здесь вы можете:\n"
        "• Просматривать каталог книг\n"
        "• Покупать книги\n"
        "• Читать купленные книги\n\n"
        "Используйте кнопки ниже или команду /help для помощи."
    )
    await message.answer(
        welcome_text,
        reply_markup=get_start_keyboard(),
        parse_mode="HTML"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📚 <b>Помощь по боту</b>\n\n"
        "Команды:\n"
        "/start - начать работу\n"
        "/help - эта справка\n"
        "/catalog - каталог книг\n"
        "/library - моя библиотека\n\n"
        f"Если у вас возникли проблемы, напишите @{settings.admin_id}"
    )
    await message.answer(help_text, parse_mode="HTML")

@router.message(Command('catalog'))
async def cmd_catalog(message: Message):
    """Обработка команды /catalog"""
    await show_catalog(message)

@router.message(Command("library"))
async def cmd_library(message: Message):
    """Обработчик команды /library"""
    await show_library(message)

@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.delete()
    await callback.message.answer(
        "🏠 Главное меню",
        reply_markup=get_start_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "about")
async def about_bot(callback: CallbackQuery):
    """Информация о боте"""
    text = (
        "📚 <b>BookBot v1.0</b>\n\n"
        "Бот для чтения и покупки книг.\n\n"
        "Разработан на:\n"
        "• Python 3.14+\n"
        "• aiogram 3\n"
        f"📧 Для связи: {settings.admin_id}"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()