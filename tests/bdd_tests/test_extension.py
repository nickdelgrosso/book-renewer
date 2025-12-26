from pytest_bdd import scenarios, given, when, then, parsers
from datetime import datetime

from src.app.app import App

scenarios('../../features/extend.feature')


# Background ################
@given(parsers.parse("the extension threshold is set to {extension_thresh:d} days"))
def extension_threshold(app: App, extension_thresh: int):
    app.set_extension_days_threshold(extension_thresh)


@given(parsers.parse("the date today is {date_str}"))
def today_date(app: App, date_str: str):        
    date = datetime.strptime(date_str, "%Y-%m-%d")
    app._clock.set_current(date)
    assert app._clock.get_current() == date


@given(parsers.parse("the warning e-mail frequency is set to {email_freq:d} days"))
def warning_frequency(email_freq: int):
    pass


@given(parsers.parse("the last e-mail was sent on {date_str}"))
def last_email_date(date_str: str):
    pass

###################################

@given(parsers.parse('"{book_title}" was checked out, is due on {due_date_str}, and has {extensions:d} extensions remaining.'))
def book_checked_out(app: App, book_title: str, due_date_str: str, extensions: int):
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    app._books_repo.add_book(title=book_title, due_on=due_date, extensions=extensions)



@when("all books are extended")
def extend_books(app: App):
    app.extend_books()


@then(parsers.parse('"{book}" is still checked out and is due later than {original_due_date}'))
def book_due_later(book, original_due_date):
    pass


@then("an extension e-mail is sent out")
def extension_email_sent():
    pass
