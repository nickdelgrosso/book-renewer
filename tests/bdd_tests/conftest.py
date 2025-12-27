from datetime import datetime, timedelta
from unittest.mock import Mock
from pytest import fixture

from src.app.app import BooksRepo, CheckedOutBook, Clock, App, CheckedOutBook, NotificationService


class InMemoryBooksRepo(BooksRepo):

    def __init__(self) -> None:
        self.__books: dict[str, CheckedOutBook] = {}
    
    def check_out_book(self, title: str, due_on: datetime, extensions: int):
        book = CheckedOutBook(
             title=title,
             due_on=due_on,
             extensions_remaining=extensions,
        )
        self.__books[book.id] = book

    def get_all_checked_out_books(self) -> list[CheckedOutBook]:
        return list(self.__books.values())
         
    def request_extension(self, book_id: str) -> tuple[bool, CheckedOutBook]:
        book = self.__books[book_id]
        if book.extensions_remaining > 0:
            updated_book = book.update(
                due_on = book.due_on + timedelta(days=14), 
                extensions_remaining = book.extensions_remaining - 1
            )
            assert updated_book.id == book.id
            self.__books[updated_book.id] = updated_book
            return True, updated_book
        else:
            return False, book
            
         

class TestClock(Clock):
        
        def set_current(self, current: datetime):
            self._current = current

        def get_current(self) -> datetime:
            return self._current




@fixture(scope="function")
def app() -> App:
     return App(
          _books_repo=InMemoryBooksRepo(),
          _clock=TestClock(),
          _notification_service = Mock(spec=NotificationService)
     )
     
     