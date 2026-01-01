
from datetime import datetime
import re

from playwright.sync_api import sync_playwright

from app.app import BooksRepo, CheckedOutBook


class StuttgartLibraryBooksRepo(BooksRepo):

    def __init__(self, username: str, password: str, headless=True) -> None:
        

        p = sync_playwright().start()
        browser = p.chromium.launch(headless=headless)
        self.page = browser.new_page()

        self.page.goto('https://stadtbibliothek-stuttgart.de/') 
        self.page.get_by_role("link", name="Mein Konto").click()

        self.page.get_by_label("Ausweisnummer").fill(username)
        self.page.get_by_label("Passwort").fill(password)
        self.page.get_by_role("button", name="Anmelden").click()

        self.page.get_by_role("link", name=re.compile(r"\bAusleihen\b")).click()

    def check_out_book(self, title: str, due_on: datetime, extensions: int):
        raise IOError("Not possible. This method only meant for testing.")

    def get_all_checked_out_books(self) -> list[CheckedOutBook]:
        rows = self.page.locator('table tbody tr')

        books: list[CheckedOutBook] = []
        for idx in range(rows.count()):
            row = rows.nth(idx)
            due_on_str = row.locator('td').nth(1).inner_text().strip()
            due_on = datetime.strptime(due_on_str, '%d.%m.%Y')
            title = row.locator('td').nth(3).inner_text().strip().replace('\n', ';  ')
            
            extension_text = rows.nth(3).locator('td').nth(4).inner_text()
            is_extendable = 'verlängerbar' in extension_text and 'nicht' not in extension_text
            book = CheckedOutBook(
                title=title,
                due_on=due_on,
                extensions_remaining=is_extendable * 6,
                id=str(idx),
            )
            books.append(book)
        return books


    def request_extension(self, book_id: str) -> tuple[bool, CheckedOutBook]:

        self.page.evaluate("() => 1")
        
        rows = self.page.locator('table tbody tr')
        row = rows.nth(int(book_id))
        
        row.locator("input[type='checkbox']").evaluate('el => el.checked = true')
        self.page.get_by_role("button", name="Markierte Medien verlängern").nth(0) # .click()
        breakpoint()





