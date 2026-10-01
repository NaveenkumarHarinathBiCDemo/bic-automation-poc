"""The setup state machine and the implement-server error path."""
import pytest

from pages.setup_page import SetupPage, STEPS
from pages.implement_banner import ImplementBanner


def test_begin_operation_is_gated_until_all_three_steps_are_set(page):
    setup = SetupPage(page)
    assert not setup.begin_enabled()
    assert setup.gate_message() == "Cannot transition"

    for step in STEPS[:-1]:
        setup.set_step(step)
        assert not setup.begin_enabled(), f"still gated after setting only up to {step}"

    setup.set_step(STEPS[-1])
    assert setup.begin_enabled()
    assert setup.gate_message() == "Ready to begin"


@pytest.mark.parametrize("step", STEPS)
def test_each_step_reports_its_chosen_value(page, step):
    setup = SetupPage(page)
    assert setup.value_of(step) == "Not Set"
    setup.set_step(step)
    assert setup.is_set(step)
    assert setup.value_of(step) != "Not Set"


def test_operation_starts_once_the_gate_opens(page):
    setup = SetupPage(page)
    for step in STEPS:
        setup.set_step(step)
    setup.begin_operation()
    toast = page.locator("#toast")
    toast.wait_for(state="visible")
    assert toast.inner_text() == "Operation started"


def test_implement_server_error_is_surfaced_and_recoverable(page):
    """The real BiC shows exactly this message. A tester's question is: does Retry work?"""
    banner = ImplementBanner(page)
    assert banner.is_visible()
    assert "implement server" in banner.message()

    banner.retry()
    assert banner.is_visible(), "one retry should not clear a connection that is still down"

    banner.retry()
    assert not banner.is_visible()
    assert "Connected" in banner.metering_text()
