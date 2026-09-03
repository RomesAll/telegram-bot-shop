from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard() -> ReplyKeyboardMarkup:
    """Reply клавиатура для старта"""
    keyboard = [
        [KeyboardButton(text="📚 Каталог книг")],
        [KeyboardButton(text="📖 Моя библиотека")],
        [KeyboardButton(text="ℹ️ О боте")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)