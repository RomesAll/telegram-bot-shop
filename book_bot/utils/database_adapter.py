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