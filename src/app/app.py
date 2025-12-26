
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime



class BooksRepo(ABC):
    
    @abstractmethod
    def add_book(self, title: str, due_on: datetime, extensions: int): ...
        

class Clock(ABC):

    @abstractmethod
    def set_current(self, current: datetime): ...

    @abstractmethod
    def get_current(self) -> datetime: ...


@dataclass
class App:
    books_repo: BooksRepo
    clock: Clock

    