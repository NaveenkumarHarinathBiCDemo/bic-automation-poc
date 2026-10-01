from pages.base_page import BasePage

STEPS = ("field", "job", "seedplan")


class SetupPage(BasePage):
    """Field -> Job -> Seed Plan gate. 'Begin Operation' stays disabled until all three are set."""

    def row(self, step: str):
        return self.page.locator(f"#row-{step}")

    def set_step(self, step: str):
        self.row(step).tap()
        return self

    def value_of(self, step: str) -> str:
        return self.row(step).locator(".val").inner_text()

    def is_set(self, step: str) -> bool:
        return self.row(step).get_attribute("data-set") == "true"

    def begin_enabled(self) -> bool:
        return self.page.locator("#begin").is_enabled()

    def gate_message(self) -> str:
        return self.page.locator("#gate").inner_text()

    def begin_operation(self):
        self.page.locator("#begin").tap()
        return self
