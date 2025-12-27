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
class BookExtension:
    book_title: str
    old_due_date: datetime
    new_due_date: datetime
    extensions_remaining: int


class NotificationService(ABC):

    @abstractmethod
    def send_extension_email(self, extensions: list[BookExtension]): ...

    @abstractmethod
    def send_warning_email(self, extensions: list[CheckedOutBook]): ...


@dataclass
class AppSettings:
    extension_days_threshold: int = 2
    extensions_remaining_threshold: int = 1
    



@dataclass
class ExtendBooksUseCase:
    books_repo: BooksRepo
    notifications_service: NotificationService
    clock: Clock

    def __call__(self, extension_days_thresh: int, extensions_remaining_thresh: int):
        current_date = self.clock.get_current()
        books = self.books_repo.get_all_checked_out_books()
        completed_book_extensions: list[BookExtension] = []
        almost_unextendable_books: list[CheckedOutBook] = []
        for book in books:
            days_remaining = (book.due_on - current_date).days
            if book.extensions_remaining <= extensions_remaining_thresh:
                almost_unextendable_books.append(book)
                

            if days_remaining <= extension_days_thresh:
                ok, book_updated = self.books_repo.request_extension(book.id)
                if not ok:
                    raise ValueError("Unsuccessful request")
                elif book_updated.due_on <= book.due_on:
                    raise ValueError("Extension didn't work")
                else:
                    extension = BookExtension(
                        book_title=book.title,
                        old_due_date=book.due_on,
                        new_due_date=book_updated.due_on,
                        extensions_remaining=book_updated.extensions_remaining
                    )
                    completed_book_extensions.append(extension)
        if completed_book_extensions:
            self.notifications_service.send_extension_email(completed_book_extensions)
        if almost_unextendable_books:
            self.notifications_service.send_warning_email(almost_unextendable_books)
    

@dataclass
class App:
    _books_repo: BooksRepo
    _clock: Clock
    _notification_service: NotificationService
    _settings: AppSettings = field(default_factory=AppSettings)


    def set_extension_days_threshold(self, value: int): 
        self._settings.extension_days_threshold = value

    def extend_books(self):
        uc = ExtendBooksUseCase(
            books_repo=self._books_repo,
            clock=self._clock,
            notifications_service=self._notification_service,
        )
        uc(
            extension_days_thresh=self._settings.extension_days_threshold,
            extensions_remaining_thresh=self._settings.extensions_remaining_threshold,
        )
        
    