from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from book_bot.utils import book_db, payment_processor
from book_bot.keyboards.inline import get_payment_buttons, get_book_card
from book_bot.states.states import BookStates

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("buy_"))
async def buy_book(callback: CallbackQuery, state: FSMContext):
    """Обработка покупки книги"""
    book_id = callback.data.split("_")[1]
    book = book_db.get_book(book_id)

    if not book:
        await callback.answer("Книга не найдена")
        return

    user_id = callback.from_user.id

    # Проверяем, не куплена ли уже книга
    if book_db.is_book_purchased(user_id, book_id):
        await callback.answer("❌ Эта книга уже куплена!", show_alert=True)
        return

    # Создаем счет
    invoice = payment_processor.create_invoice(book_id, book['price'], user_id)

    text = (
        f"💳 <b>Оформление покупки</b>\n\n"
        f"Книга: {book['title']}\n"
        f"Автор: {book['author']}\n"
        f"Сумма: {book['price']}₽\n\n"
        f"Для оплаты нажмите кнопку ниже.\n"
        f"Счет действителен 10 минут."
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_payment_buttons(invoice['invoice_id'], book_id),
        parse_mode="HTML"
    )
    await state.set_state(BookStates.purchasing)
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
    """Обработка платежа"""
    invoice_id = callback.data.split("_")[1]
    user_id = callback.from_user.id

    # В реальном проекте здесь был бы запрос к платежной системе
    payment_success = payment_processor.process_payment(invoice_id)

    if payment_success:
        # Находим книгу по invoice_id
        # В реальности нужно хранить связь invoice -> book_id
        # Для примера используем упрощенный подход
        book_id = "book_1"  # В реальности получаем из БД
        book_db.purchase_book(user_id, book_id)

        book = book_db.get_book(book_id)
        await callback.message.edit_text(
            f"✅ <b>Покупка успешно завершена!</b>\n\n"
            f"Книга \"{book['title']}\" теперь в вашей библиотеке.\n"
            f"Вы можете начать чтение прямо сейчас.",
            reply_markup=get_book_card(book_id, True),
            parse_mode="HTML"
        )
        await state.clear()
    else:
        await callback.message.edit_text(
            "❌ <b>Ошибка оплаты</b>\n\n"
            "Платеж не прошел. Попробуйте позже или свяжитесь с поддержкой.",
            parse_mode="HTML"
        )

    await callback.answer()