"""Base page object. Every page inherits the Playwright `page` handle plus shared waits."""


class BasePage:
    def __init__(self, page):
        self.page = page

    def title_text(self) -> str:
        return self.page.locator("#screen-title").inner_text()

    def screenshot(self, name: str):
        self.page.screenshot(path=f"reports/{name}.png")
