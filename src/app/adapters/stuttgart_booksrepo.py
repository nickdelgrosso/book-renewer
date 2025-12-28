

from datetime import datetime
from src.app.app import BooksRepo, CheckedOutBook


class StuttgartLibraryBooksRepo(BooksRepo):

    def __init__(self) -> None:
        ...

    def check_out_book(self, title: str, due_on: datetime, extensions: int):
        raise IOError("Not possible. This method only meant for testing.")

    def get_all_checked_out_books(self) -> list[CheckedOutBook]:
        ...

    def request_extension(self, book_id: str) -> tuple[bool, CheckedOutBook]:
        ...