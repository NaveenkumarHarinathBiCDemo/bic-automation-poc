"""iPad integration + navigation: device emulation, tab switching, menu structure."""
import pytest

from pages.nav_bar import NavBar, TABS


def test_runs_on_an_emulated_ipad_in_landscape(page):
    """Proves the suite drives a touch device in landscape, not a desktop browser."""
    vp = page.viewport_size
    assert vp["width"] > vp["height"], "BiC is landscape-locked; the harness must be too"
    assert page.evaluate("navigator.maxTouchPoints") > 0, "touch must be enabled"
    assert "iPad" in page.evaluate("navigator.userAgent")


@pytest.mark.parametrize("tab", TABS)
def test_each_tab_opens_its_own_panel(page, tab):
    nav = NavBar(page).open_tab(tab)
    assert nav.is_selected(tab)
    assert nav.panel_visible(tab)
    for other in (t for t in TABS if t != tab):
        assert not nav.panel_visible(other), f"{other} should be hidden when {tab} is open"


def test_menu_lists_every_expected_section(page):
    items = NavBar(page).open_menu().menu_items()
    assert items == [
        "Operation", "System Checks", "Notification Log", "Service and Support",
        "Implement Profiles", "ECU Configuration", "Software and Updates",
        "Connection Settings", "Data Management",
    ]


def test_menu_navigates_to_ecu_configuration(page):
    nav = NavBar(page).open_menu().go_to("ecu-configuration")
    assert nav.title_text() == "ECU Configuration"


def test_notifications_tab_shows_fault_severities(page):
    NavBar(page).open_tab("notifications")
    rows = page.locator("#panel-notifications tbody tr")
    assert rows.count() == 3
    assert page.locator(".sev-high").count() == 2
