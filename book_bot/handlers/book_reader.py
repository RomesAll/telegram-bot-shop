from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from book_bot.utils import book_db
from book_bot.keyboards.inline import get_library_buttons, get_reader_buttons
from book_bot.states.states import BookStates

router = Router()

# Хранилище текущих страниц чтения
current_reader_pages = {}  # user_id: {book_id: page}


async def show_library(message: Message):
    """Показать библиотеку пользователя"""
    user_id = message.from_user.id
    books = book_db.get_user_library(user_id)

    if not books:
        await message.answer(
            "📭 У вас пока нет купленных книг.\n"
            "Перейдите в каталог, чтобы приобрести книги."
        )
        return

    text = "<b>Ваша библиотека</b>\n\nВыберите книгу для чтения:"
    await message.answer(
        text,
        reply_markup=get_library_buttons(books),
        parse_mode="HTML"
    )


@router.callback_query(lambda c: c.data == "my_library")
async def show_library_callback(callback: CallbackQuery):
    """Показать библиотеку из callback"""
    user_id = callback.from_user.id
    books = book_db.get_user_library(user_id)

    if not books:
        await callback.message.edit_text(
            "📭 У вас пока нет купленных книг.\n"
            "Перейдите в каталог, чтобы приобрести книги."
        )
        await callback.answer()
        return

    text = "📖 <b>Ваша библиотека</b>\n\nВыберите книгу для чтения:"
    await callback.message.edit_text(
        text,
        reply_markup=get_library_buttons(books),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("read_"))
async def read_book(callback: CallbackQuery, state: FSMContext):
    """Начать чтение книги"""
    book_id = callback.data.split("_")[1]
    book = book_db.get_book(book_id)

    if not book:
        await callback.answer("Книга не найдена")
        return

    user_id = callback.from_user.id
    if not book_db.is_book_purchased(user_id, book_id):
        await callback.answer("❌ Эта книга не куплена. Приобретите её в каталоге.")
        return

    # Инициализируем страницу для книги
    if user_id not in current_reader_pages:
        current_reader_pages[user_id] = {}
    if book_id not in current_reader_pages[user_id]:
        current_reader_pages[user_id][book_id] = 1

    current_page = current_reader_pages[user_id][book_id]
    total_pages = book.get('pages', 100)  # В реальности считаем из содержимого

    # Получаем содержимое страницы (в реальности из файла)
    content = book.get('content', 'Содержание книги...')

    # Разбиваем на страницы (в реальности по абзацам или символам)
    page_size = 1000  # символов на страницу
    pages = [content[i:i + page_size] for i in range(0, len(content), page_size)]
    total_pages = len(pages)

    if current_page > total_pages:
        current_page = total_pages

    page_content = pages[current_page - 1] if pages else "Конец книги"

    text = (
        f"📖 <b>{book['title']}</b>\n"
        f"👤 {book['author']}\n"
        f"{'-' * 30}\n\n"
        f"{page_content}\n\n"
        f"{'-' * 30}\n"
        f"📄 Страница {current_page} из {total_pages}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_reader_buttons(book_id, current_page, total_pages),
        parse_mode="HTML"
    )
    await state.set_state(BookStates.reading)
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("reader_page_"))
async def reader_page(callback: CallbackQuery):
    """Переключение страниц при чтении"""
    parts = callback.data.split("_")
    book_id = parts[2]
    page = int(parts[3])

    book = book_db.get_book(book_id)
    if not book:
        await callback.answer("Книга не найдена")
        return

    user_id = callback.from_user.id
    current_reader_pages[user_id][book_id] = page

    # Получаем содержимое страницы
    content = book.get('content', 'Содержание книги...')
    page_size = 1000
    pages = [content[i:i + page_size] for i in range(0, len(content), page_size)]
    total_pages = len(pages)

    if page > total_pages:
        page = total_pages

    page_content = pages[page - 1] if pages else "Конец книги"

    text = (
        f"📖 <b>{book['title']}</b>\n"
        f"👤 {book['author']}\n"
        f"{'-' * 30}\n\n"
        f"{page_content}\n\n"
        f"{'-' * 30}\n"
        f"📄 Страница {page} из {total_pages}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_reader_buttons(book_id, page, total_pages),
        parse_mode="HTML"
    )
    await callback.answer()