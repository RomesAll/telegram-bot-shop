from book_bot.utils.database_adapter import BookDatabase
from book_bot.utils.payment_adapter import PaymentProcessor

book_db = BookDatabase()
payment_processor = PaymentProcessor()

__version__ = 'v1.0.0'
__author__ = 'RomesAll'
__all__ = [
    'book_db',
    'payment_processor'
]