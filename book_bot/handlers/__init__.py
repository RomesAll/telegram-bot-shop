from aiogram import Dispatcher

from book_bot.handlers.book_reader import router as book_reader_router
from book_bot.handlers.catalog import router as catalog_router
from book_bot.handlers.purchase import router as purchase_router
from book_bot.handlers.start import router as start_router

def register_router(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(catalog_router)
    dp.include_router(book_reader_router)
    dp.include_router(purchase_router)

__version__ = 'v1.0.0'
__author__ = 'RomesAll'
__all__ = [
    'register_router'
]