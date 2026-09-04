from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from book_bot.utils import book_db
from book_bot.keyboards.inline import get_catalog_buttons, get_book_card
from book_bot.states.states import BookStates

router = Router()
current_pages = {}

async def show_catalog(msg: Message, page: int = 0):
    """Показать каталог книг"""
    books = book_db.get_all_books()
    if not books:
        await msg.answer('В каталоге пока нет книг')
        return
    current_pages[msg.from_user.id] = page
    await msg.answer(
        "📚 <b>Каталог книг</b>\n\nВыберите книгу:",
        reply_markup=get_catalog_buttons(books, page),
        parse_mode="HTML"
    )


@router.callback_query(lambda c: c.data and c.data.startswith("page_"))
async def catalog_page(callback: CallbackQuery):
    """Переключение страниц каталога"""
    page = int(callback.data.split("_")[1])
    books = book_db.get_all_books()
    current_pages[callback.from_user.id] = page

    await callback.message.edit_text(
        "📚 <b>Каталог книг</b>\n\nВыберите книгу:",
        reply_markup=get_catalog_buttons(books, page),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("book_"))
async def book_detail(callback: CallbackQuery):
    """Детальная информация о книге"""
    book_id = callback.data.split("_")[1]
    book = book_db.get_book(book_id)

    if not book:
        await callback.answer("Книга не найдена")
        return

    user_id = callback.from_user.id
    is_purchased = book_db.is_book_purchased(user_id, book_id)

    text = (
        f"{book.get('cover', '📚')} <b>{book['title']}</b>\n\n"
        f"👤 Автор: {book['author']}\n"
        f"📖 Жанр: {book.get('genre', 'Не указан')}\n"
        f"💰 Цена: {book['price']}₽\n"
        f"📄 Страниц: {book.get('pages', 'Не указано')}\n\n"
        f"📝 Описание:\n{book['description']}\n\n"
        f"{'✅ Книга куплена' if is_purchased else '❌ Книга не куплена'}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_book_card(book_id, is_purchased),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "catalog")
async def show_catalog_callback(callback: CallbackQuery):
    """Показать каталог из callback"""
    books = book_db.get_all_books()
    await callback.message.edit_text(
        "📚 <b>Каталог книг</b>\n\nВыберите книгу:",
        reply_markup=get_catalog_buttons(books, 0),
        parse_mode="HTML"
    )
    await callback.answer()