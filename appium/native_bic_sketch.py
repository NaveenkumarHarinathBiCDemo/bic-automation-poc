"""
NOT RUN IN THIS POC -- this is the design, and saying so is the point.

Playwright drives browsers. BiC is a native .NET MAUI iPad app, so Playwright
cannot touch it. The correct tool is Appium with the XCUITest driver.

What this file demonstrates is that the swap is confined to ONE layer. Compare
`ConnectionSettingsPage` in pages/ with the class below: the method names, the
assertions, the test bodies and the whole CI pipeline are identical. Only the
locator strategy and the driver change.

Prerequisites I would need on a Mac to make this live:
    Xcode + command line tools
    appium + the XCUITest driver        (appium driver install xcuitest)
    WebDriverAgent signed for the iPad  (one-time, needs a provisioning profile)
    A real cart or a simulated implement server on 192.168.200.1

Accessibility identifiers are the real dependency: a .NET MAUI control exposes
`AutomationId`, which surfaces to XCUITest as `accessibility id`. Where BiC's
controls lack one, my first ask of the dev team would be to add them -- that is
cheap at build time and the difference between a stable suite and a flaky one.
"""

from appium.options.ios import XCUITestOptions   # noqa: F401  (design reference)


def ipad_driver():
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = "iPad Pro 11-inch"
    options.platform_version = "18.0"
    options.bundle_id = "com.bourgault.aircontrol"   # read from the shipped app bundle
    options.no_reset = True
    # from appium import webdriver
    # return webdriver.Remote("http://127.0.0.1:4723", options=options)


class NativeConnectionSettingsPage:
    """Same contract as pages/connection_settings_page.py -- different locators only."""

    IP = ("accessibility id", "implementIpAddress")
    STREAM = ("accessibility id", "dataStreamPort")
    SERVER = ("accessibility id", "dataServerPort")
    SAVE = ("accessibility id", "saveConnectionSettings")

    def __init__(self, driver):
        self.driver = driver

    def values(self) -> dict:
        return {
            "ip": self.driver.find_element(*self.IP).get_attribute("value"),
            "stream": self.driver.find_element(*self.STREAM).get_attribute("value"),
            "server": self.driver.find_element(*self.SERVER).get_attribute("value"),
        }

    def set_ip(self, value: str):
        field = self.driver.find_element(*self.IP)
        field.clear()
        field.send_keys(value)
        return self

    def save_enabled(self) -> bool:
        return self.driver.find_element(*self.SAVE).get_attribute("enabled") == "true"

    def save(self):
        self.driver.find_element(*self.SAVE).click()
        return self


# The test above it would not change at all:
#
#   def test_invalid_ip_is_rejected_and_blocks_save(connection):
#       connection.set_ip("999.1.1.1")
#       assert not connection.save_enabled()
