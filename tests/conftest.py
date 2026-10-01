"""
Shared fixtures.

The key idea for the interview: `ipad_context` uses Playwright's *device emulation*.
We do not launch a desktop browser and shrink it -- we adopt the real iPad Pro 11
descriptor: its viewport, device scale factor, user agent, and crucially
`has_touch=True`, which is why every page object calls .tap() instead of .click().
Swapping this one fixture for an Appium XCUITest session is what takes this suite
from mobile-web to the native BiC app; nothing below the fixture changes.
"""
import os
import socket
import threading
import functools
import http.server
import socketserver
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = ROOT / "app"
REPORTS = ROOT / "reports"
HEADLESS = os.getenv("HEADED", "0") != "1"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    """Serve app/ over real HTTP so the suite exercises a network stack, not file://."""
    port = _free_port()
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(APP_DIR))
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{port}/index.html"
    httpd.shutdown()


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=HEADLESS,
        # ms pause between actions, for demos
        slow_mo=int(os.getenv("SLOWMO", "0")),
    )
    yield browser
    browser.close()


@pytest.fixture
def ipad_context(playwright_instance, browser):
    """iPad Pro 11 landscape, touch enabled -- Playwright's own device descriptor."""
    device = dict(playwright_instance.devices["iPad Pro 11"])
    # landscape; BiC is landscape-locked
    device["viewport"] = {"width": 1194, "height": 834}
    device["screen"] = {"width": 1194, "height": 834}
    ctx = browser.new_context(**device)
    yield ctx
    ctx.close()


@pytest.fixture
def page(ipad_context, base_url, request):
    page = ipad_context.new_page()
    page.goto(base_url)
    yield page
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        REPORTS.mkdir(exist_ok=True)
        page.screenshot(path=str(REPORTS / f"FAIL-{request.node.name}.png"))
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach each phase's result to the node so `page` can screenshot on failure."""
    outcome = yield
    setattr(item, "rep_" + call.when, outcome.get_result())
