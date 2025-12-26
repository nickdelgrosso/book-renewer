from datetime import datetime
from pytest import fixture

from src.app.app import BooksRepo


class InMemoryBooksRepo(BooksRepo):
    
    def add_book(self, title: str, due_on: datetime, extensions: int):
        ...
    

@fixture(scope="function")
def books_repo() -> BooksRepo:
    return InMemoryBooksRepo()
