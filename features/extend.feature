Feature: Extend Book Borrows

    Extend the borrowing time if possible, for checked-out books that might become overdue.


Background:
    Given the extension threshold is set to 3 days
    Given the date today is 2025-08-20
    Given the warning e-mail frequency is set to 2 days
    Given the last e-mail was sent on 2025-08-18


Scenario: A book is about to be overdue and can still be extended at least twice.
    Given "Catch-22" was checked out, is due on 2025-08-22, and has 3 extensions remaining.
    When all books are extended
    Then "Catch-22" is still checked out and is due later than 2025-08-22
    And an extension e-mail is sent out
    

Scenario: A book is about to be overdue and this is the last time it can be extended.
    Given "Catch-22" was checked out, is due on 2025-08-22, and has 1 extensions remaining.
    When all books are extended
    Then "Catch-22" is still checked out and is due later than 2025-08-22
    And a warning e-mail is sent out


@skip
Scenario: A book is about to be overdue and cannot be extended again.
    Given "Catch-22" was checked out, is due on 2025-08-22, and has 0 extensions remaining.
    When all books are extended
    Then "Catch-22" is still checked out and is due on 2025-08-22
    And no e-mail is sent out

@skip
Scenario: A mix of statuses
    Given "Catch-22" was checked out, is due on 2025-08-22, and has 3 extensions remaining.
    Given "A Fault in Our Stars" was checked out, is due on 2025-08-30, and has 3 extensions remaining.
    Given "Hamlet" was checked out, is due on 2025-08-22, and has 0 extensions remaining.
    When all books are extended
    Then "Catch-22" is still checked out is due later than 2025-08-22
    Then "A Fault in Our Stars" is still checked out is and is due on 2025-08-30
    Then "Hamlet" is still checked out is and is due on 2025-08-30
    And an extension e-mail is sent out
    And a warning e-mail is sent out
