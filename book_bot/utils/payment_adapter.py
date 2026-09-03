import random


class PaymentProcessor:
    """Класс адаптер для обработки платежей"""
    @staticmethod
    def create_invoice(book_id: str, price: int, user_id: int) -> dict:
        """Создает счет для оплаты (mock)"""
        return {
            'invoice_id': f'inv_{user_id}_{book_id}_{random.randint(1000, 9999)}',
            'book_id': book_id,
            'amount': price,
            'status': 'pending',
            'payment_url': f'https://mock-payment.com/pay/{random.randint(100000, 999999)}'
        }

    @staticmethod
    def process_payment(invoice_id: str) -> bool:
        """Обрабатывает платеж (mock)"""
        # Имитация успешной оплаты в 95% случаев
        return random.random() < 0.95
