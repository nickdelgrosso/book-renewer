from datetime import datetime
from pytest import fixture

from src.app.app import BooksRepo, CheckedOutBook, Clock, App, CheckedOutBook


class InMemoryBooksRepo(BooksRepo):

    def __init__(self) -> None:
        self.__books: dict[str, CheckedOutBook] = {}
    
    def check_out_book(self, title: str, due_on: datetime, extensions: int):
        book = CheckedOutBook(
             title=title,
             due_on=due_on,
             extensions_remaining=extensions,
        )
        self.__books[title] = book

    def get_all_checked_out_books(self) -> list[CheckedOutBook]:
        return list(self.__books.values())
         
    

class TestClock(Clock):
        
        def set_current(self, current: datetime):
            self._current = current

        def get_current(self) -> datetime:
            return self._current




@fixture(scope="function")
def app() -> App:
     return App(
          _books_repo=InMemoryBooksRepo(),
          _clock=TestClock()
     )
     
     