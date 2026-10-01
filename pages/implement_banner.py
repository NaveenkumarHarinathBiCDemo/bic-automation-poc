from pages.base_page import BasePage


class ImplementBanner(BasePage):
    """The 'cannot reach the implement server' banner and its Retry control."""

    def is_visible(self) -> bool:
        return self.page.locator("#banner").is_visible()

    def message(self) -> str:
        return self.page.locator("#banner span").inner_text()

    def retry(self):
        self.page.locator("#retry").tap()
        return self

    def metering_text(self) -> str:
        return self.page.locator("#metering-empty").inner_text()
