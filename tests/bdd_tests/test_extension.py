from pytest_bdd import scenarios, given, when, then, parsers
from datetime import date, datetime

from src.app.app import BooksRepo, Clock

scenarios('../../features/extend.feature')


# Background ################
@given("the extension threshold is set to 3 days")
def extension_threshold():
    pass


@given(parsers.parse("the date today is {date_str}"))
def today_date(clock: Clock, date_str: str):        
    date = datetime.strptime(date_str, "%Y-%m-%d")
    clock.set_current(date)
    assert clock.get_current() == date


@given("the warning e-mail frequency is set to 2 days")
def warning_frequency():
    pass


@given("the last e-mail was sent on 2025-08-18")
def last_email_date():
    pass

###################################

@given(parsers.parse('"{book_title}" was checked out, is due on {due_date_str}, and has {extensions:d} extensions remaining.'))
def book_checked_out(books_repo: BooksRepo, book_title: str, due_date_str: str, extensions: int):
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    books_repo.add_book(title=book_title, due_on=due_date, extensions=extensions)



@when("all books are extended")
def extend_books():
    pass


@then(parsers.parse('"{book}" is still checked out and is due later than {original_due_date}'))
def book_due_later(book, original_due_date):
    pass


@then("an extension e-mail is sent out")
def extension_email_sent():
    pass
