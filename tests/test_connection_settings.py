"""Form handling + validation on the screen that points the iPad at the implement."""
import pytest

from pages.nav_bar import NavBar
from pages.connection_settings_page import (
    ConnectionSettingsPage, WIFI_DEFAULTS, ETHERNET_DEFAULTS,
)


@pytest.fixture
def connection(page):
    NavBar(page).open_menu().go_to("connection")
    return ConnectionSettingsPage(page)


def test_wifi_defaults_populate_the_documented_endpoint(connection):
    assert connection.use_wifi_defaults().values() == WIFI_DEFAULTS


def test_ethernet_defaults_differ_from_wifi(connection):
    assert connection.use_ethernet_defaults().values() == ETHERNET_DEFAULTS


def test_save_is_blocked_until_something_actually_changes(connection):
    assert not connection.save_enabled(), "Save must stay disabled on a pristine form"
    connection.set_stream_port("44100")
    assert connection.save_enabled()


@pytest.mark.parametrize("bad_ip", ["192.168.200", "999.1.1.1", "not-an-ip", ""])
def test_invalid_ip_is_rejected_and_blocks_save(connection, bad_ip):
    connection.set_ip(bad_ip)
    assert connection.ip_error_visible(), f"{bad_ip!r} should raise a validation error"
    assert not connection.save_enabled()


@pytest.mark.parametrize("bad_port", ["0", "65536", "abc"])
def test_out_of_range_port_is_rejected(connection, bad_port):
    connection.set_stream_port(bad_port)
    assert connection.port_error_visible()
    assert not connection.save_enabled()


def test_valid_change_saves_and_confirms(connection):
    connection.set_ip("192.168.200.25")
    assert connection.save_enabled()
    connection.save()
    assert connection.toast_text() == "Saved"
    assert not connection.save_enabled(), "Form should be clean again after saving"


def test_undo_restores_the_last_saved_values(connection):
    connection.set_ip("10.0.0.5")
    connection.undo()
    assert connection.values()["ip"] == WIFI_DEFAULTS["ip"]
