from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import Field, dataclass, field, replace
from datetime import datetime
from typing import Any, NamedTuple
from uuid import uuid4

@dataclass(frozen=True)
class CheckedOutBook:
    title: str
    due_on: datetime
    extensions_remaining: int
    id: str = field(default_factory=lambda: str(uuid4())[:16])

    def update(self, **kwargs) -> CheckedOutBook:
        return replace(self, **kwargs)


class BooksRepo(ABC):
    
    @abstractmethod
    def check_out_book(self, title: str, due_on: datetime, extensions: int): ...

    @abstractmethod
    def get_all_checked_out_books(self) -> list[CheckedOutBook]: ...
        
    @abstractmethod
    def request_extension(self, book_id: str) -> tuple[bool, CheckedOutBook]: ...


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
        current_date = self.clock.get_current()
        books = self.books_repo.get_all_checked_out_books()
        for book in books:
            days_remaining = (book.due_on - current_date).days
            if days_remaining <= extension_days_thresh:
                ok, book_updated = self.books_repo.request_extension(book.id)
                if not ok:
                    raise ValueError("Unsuccessful request")
                elif book_updated.due_on <= book.due_on:
                    raise ValueError("Extension didn't work")

    

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
        
    