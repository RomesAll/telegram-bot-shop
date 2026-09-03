import json


class BookDatabase:
    """Класс адаптер для взаимодействия с данными книг"""
    def __init__(self, data_path: str = 'data/books.json'):
        self.data_path = data_path
        self.books = self._load_books()
        self.user_lib = {}
        self.purchases = {}

    def _load_books(self) -> list[dict]:
        """Загрузка книг из хранилища"""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                return data.get('books', [])
        except FileNotFoundError:
            return []

    def get_all_books(self) -> list[dict]:
        """Получить все книги"""
        return self.books

    def get_book(self, book_id: str) -> dict | None:
        """Получить книгу по id"""
        for book in self.books:
            if book['id'] == book_id:
                return book
        return None

    def get_books_by_genre(self, genre: str) -> list[dict]:
        """Получить книгу по жанру"""
        return [b for b in self.books if b.get('genre') == genre]

    def is_book_purchased(self, user_id: int, book_id: str) -> bool:
        """Куплена ли эта книга"""
        return user_id in self.user_lib and book_id in self.user_lib[user_id]

    def purchase_book(self, user_id: int, book_id: str) -> bool:
        """Покупка книги"""
        if not(book := self.get_book(book_id)):
            return False

        if user_id not in self.user_lib:
            self.user_lib[user_id] = []

        if book_id not in self.user_lib[user_id]:
            self.user_lib[user_id].append(book_id)

        if user_id not in self.purchases:
            self.purchases[user_id] = []
        self.purchases[user_id].append({
            'book_id': book_id,
            'title': book['title'],
            'price': book['price']
        })
        return True

    def get_user_library(self, user_id: int):
        """Получить библиотеку пользователя"""
        if user_id not in self.user_lib:
            return []
        return [self.get_book(book_id) for book_id in self.user_lib[user_id]
                if self.get_book(book_id)]