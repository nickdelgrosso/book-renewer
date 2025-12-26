
from abc import ABC, abstractmethod
from dataclasses import Field, dataclass, field
from datetime import datetime
from typing import Any, NamedTuple

@dataclass
class CheckedOutBook:
    title: str
    due_on: datetime
    extensions_remaining: int


class BooksRepo(ABC):
    
    @abstractmethod
    def check_out_book(self, title: str, due_on: datetime, extensions: int): ...

    @abstractmethod
    def get_all_checked_out_books(self) -> list[CheckedOutBook]: ...
        

class Clock(ABC):

    @abstractmethod
    def set_current(self, current: datetime): ...

    @abstractmethod
    def get_current(self) -> datetime: ...



@dataclass
class AppSettings:
    extension_days_threshold: int = 2
    

@dataclass
class ExtendBooksUseCase:
    books_repo: BooksRepo
    clock: Clock

    def __call__(self, extension_days_thresh: int):
        ...
    

@dataclass
class App:
    _books_repo: BooksRepo
    _clock: Clock
    _settings: AppSettings = field(default_factory=AppSettings)


    def set_extension_days_threshold(self, value: int): 
        self._settings.extension_days_threshold = value

    def extend_books(self):
        uc = ExtendBooksUseCase(
            books_repo=self._books_repo,
            clock=self._clock,
        )
        uc(extension_days_thresh=self._settings.extension_days_threshold)
        
    