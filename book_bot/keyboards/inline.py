from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню"""
    buttons = [
        [InlineKeyboardButton(text="📚 Каталог книг", callback_data="catalog")],
        [InlineKeyboardButton(text="📚 Моя библиотека", callback_data="my_library")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_book_card(book_id: str, is_purchased: bool = False) -> InlineKeyboardMarkup:
    """Карточка книги с кнопками"""
    buttons = []
    if is_purchased:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Читать',
                    callback_data=f'read_{book_id}'
                )
            ]
        )
    else:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='💰 Купить',
                    callback_data=f'buy_{book_id}'
                )
            ]
        )
    buttons.append([
        InlineKeyboardButton(text="<- Назад", callback_data="catalog")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_catalog_buttons(books: list[dict], page: int = 0, per_page: int = 5) -> InlineKeyboardMarkup:
    """Кнопки каталога с пагинацией"""
    buttons = []
    start = page * per_page
    end = min(start + per_page, len(books))
    for book in books[start:end]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{book.get('cover', '📚')} {book['title']} - {book['price']}₽",
                callback_data=f"book_{book['id']}"
            )
        ])
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<-", callback_data=f"page_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text=f"{page + 1}", callback_data="current_page"))
    if end < len(books):
        nav_buttons.append(InlineKeyboardButton(text="->", callback_data=f"page_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_library_buttons(books: list[dict]) -> InlineKeyboardMarkup:
    """Библиотека пользователя"""
    buttons = []
    for book in books:
        buttons.append([
            InlineKeyboardButton(
                text=f"{book.get('cover', '📚')} {book['title']}",
                callback_data=f"read_{book['id']}"
            )
        ])

    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_reader_buttons(book_id: str, current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    """Кнопки для чтения книги с пагинацией"""
    buttons = []

    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"reader_page_{book_id}_{current_page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="current_reader_page"))

    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"reader_page_{book_id}_{current_page + 1}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([InlineKeyboardButton(text="В библиотеку", callback_data="my_library")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_payment_buttons(invoice_id: str, book_id: str) -> InlineKeyboardMarkup:
    """Кнопки оплаты"""
    buttons = [
        [InlineKeyboardButton(text="💳 Оплатить", callback_data=f"pay_{invoice_id}")],
        [InlineKeyboardButton(text="Х Отмена", callback_data=f"book_{book_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)