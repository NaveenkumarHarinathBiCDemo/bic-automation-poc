from pages.base_page import BasePage

WIFI_DEFAULTS = {"ip": "192.168.200.1", "stream": "44000", "server": "5000"}
ETHERNET_DEFAULTS = {"ip": "192.168.100.1", "stream": "44001", "server": "5001"}


class ConnectionSettingsPage(BasePage):
    """Implement IP address and the two ports the iPad uses to reach the cart."""

    IP = "#implement-ip"
    STREAM = "#stream-port"
    SERVER = "#server-port"

    def use_wifi_defaults(self):
        self.page.locator("#wifi-defaults").tap()
        return self

    def use_ethernet_defaults(self):
        self.page.locator("#ethernet-defaults").tap()
        return self

    def values(self) -> dict:
        return {
            "ip": self.page.input_value(self.IP),
            "stream": self.page.input_value(self.STREAM),
            "server": self.page.input_value(self.SERVER),
        }

    def set_ip(self, value: str):
        self.page.fill(self.IP, value)
        return self

    def set_stream_port(self, value: str):
        self.page.fill(self.STREAM, value)
        return self

    def ip_error_visible(self) -> bool:
        return self.page.locator("#ip-error").is_visible()

    def port_error_visible(self) -> bool:
        return self.page.locator("#port-error").is_visible()

    def save_enabled(self) -> bool:
        return self.page.locator("#save").is_enabled()

    def save(self):
        self.page.locator("#save").tap()
        return self

    def undo(self):
        self.page.locator("#undo").tap()
        return self

    def toast_text(self) -> str:
        toast = self.page.locator("#toast")
        toast.wait_for(state="visible", timeout=3000)
        return toast.inner_text()
