from datetime import datetime
from pytest import fixture

from src.app.app import BooksRepo, Clock, App


class InMemoryBooksRepo(BooksRepo):
    
    def add_book(self, title: str, due_on: datetime, extensions: int):
        ...
    

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
     
     