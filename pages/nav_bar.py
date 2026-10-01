from pages.base_page import BasePage

TABS = ("metering", "map", "metrics", "notifications")


class NavBar(BasePage):
    """The four operation tabs across the top of the BiC screen."""

    def tab(self, name: str):
        return self.page.locator(f'[role="tab"][data-tab="{name}"]')

    def open_tab(self, name: str):
        self.tab(name).tap()          # tap(), not click() — this is a touch device
        return self

    def is_selected(self, name: str) -> bool:
        return self.tab(name).get_attribute("aria-selected") == "true"

    def panel_visible(self, name: str) -> bool:
        return self.page.locator(f"#panel-{name}").is_visible()

    def open_menu(self):
        self.page.locator("#hamburger").tap()
        self.page.locator("#menu").wait_for(state="visible")
        return self

    def menu_items(self) -> list[str]:
        return self.page.locator("#menu .item").all_inner_texts()

    def go_to(self, screen: str):
        self.page.locator(f'#menu .item[data-screen="{screen}"]').tap()
        return self
