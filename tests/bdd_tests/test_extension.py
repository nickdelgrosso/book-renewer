from pytest_bdd import scenarios, given, when, then, parsers


scenarios('../../features/extend.feature')


@given("the extension threshold is set to 3 days")
def extension_threshold():
    pass


@given("the date today is 2025-08-20")
def today_date():
    pass


@given("the warning e-mail frequency is set to 2 days")
def warning_frequency():
    pass


@given("the last e-mail was sent on 2025-08-18")
def last_email_date():
    pass


@given(parsers.parse('"{book}" was checked out, is due on {due_date}, and has {extensions:d} extensions remaining.'))
def book_checked_out(book, due_date, extensions):
    pass


@when("all books are extended")
def extend_books():
    pass


@then(parsers.parse('"{book}" is still checked out and is due later than {original_due_date}'))
def book_due_later(book, original_due_date):
    pass


@then("an extension e-mail is sent out")
def extension_email_sent():
    pass
