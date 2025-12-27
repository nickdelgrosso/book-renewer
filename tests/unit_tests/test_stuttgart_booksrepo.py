from datetime import datetime, timedelta

from pytest import raises, fixture

from src.app.adapters.stuttgart_booksrepo import StuttgartLibraryBooksRepo



@fixture
def repo() -> StuttgartLibraryBooksRepo:
    return StuttgartLibraryBooksRepo()

def test_cannot_checkout_new_books(repo: StuttgartLibraryBooksRepo):
    with raises(IOError):
        repo.check_out_book(title='a', due_on=datetime.now() + timedelta(days=10), extensions=4)
