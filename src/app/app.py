
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime



class BooksRepo(ABC):
    
    @abstractmethod
    def add_book(self, title: str, due_on: datetime, extensions: int): ...
        



@dataclass
class App:
    books_repo: BooksRepo

    