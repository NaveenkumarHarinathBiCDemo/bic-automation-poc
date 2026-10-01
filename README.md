# BiC UI Regression — automation POC

A working Playwright + pytest suite built around the **Bourgault Intelligent
Control** workflow, driven on an **emulated iPad in landscape**, wired into
**GitHub Actions** with manual, push and scheduled triggers.

```
26 tests · ~12s · Page Object Model · HTML report · screenshots on failure
```

## Why the target is a mock, and why that is the honest choice

BiC is a native **.NET MAUI** iPad application. Playwright drives browsers; it
cannot automate a native app. Pretending otherwise would be the wrong answer to
give a test engineer.

So `app/index.html` is a faithful harness of the BiC screens I could observe from
the shipped App Store build — the four operation tabs, the nine-item system menu,
the `Field → Job → Seed Plan → Begin Operation` gate with its *"Cannot transition"*
guard, Connection Settings carrying the real defaults (`192.168.200.1`, stream
port `44000`, data server port `5000`), the fault list, and the
*"An error occurred while loading data from implement server…"* banner with Retry.

The suite exercises that harness exactly as it would exercise the real thing.
`appium/native_bic_sketch.py` shows the one layer that changes to point this at
the native app: **locators and driver**. Page objects, tests, fixtures, reporting
and CI are untouched.

## Layout

```
app/                     the BiC harness under test (single HTML file)
pages/                   Page Object Model — one class per screen
  base_page.py           shared handle + screenshot helper
  nav_bar.py             four tabs, hamburger menu
  setup_page.py          the Field/Job/Seed Plan gate
  connection_settings_page.py
  implement_banner.py    the connection-error banner and Retry
tests/
  conftest.py            iPad device emulation, local HTTP server, failure screenshots
  test_navigation.py     device emulation, tab isolation, menu structure
  test_connection_settings.py   form fill, IP/port validation, save/undo
  test_setup_workflow.py state machine gate, error recovery
appium/native_bic_sketch.py     how this points at the real native app
.github/workflows/ci.yml        push + manual dispatch + weekday cron
COMMANDS.md              every shell command used
```

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
export PYTHONPATH=.
python -m pytest            # or:  HEADED=1 python -m pytest   to watch it
```

Report lands in `reports/report.html`.

## What each part is meant to show

| Area | Where to look |
|---|---|
| Python | page objects, fixtures, parametrisation, type hints |
| Playwright | device emulation, `tap()` on a touch context, auto-waiting locators |
| Mobile testing | `ipad_context` fixture; landscape assertion; `navigator.maxTouchPoints` |
| Test design | POM, one assertion theme per test, negative cases, a real state machine |
| CI/CD | three triggers, suite selection input, artifact upload, step summary |
| Linux/shell | `COMMANDS.md`, `run.sh` |
| Git | branch → commit → PR → CI gate |

## Known limits — say these before they ask

- The target is a harness, not the shipped app. No MQTT, no protobuf, no CAN.
- Device emulation is not a physical iPad. Real-device gaps it cannot catch:
  memory pressure, backgrounding, sunlight legibility, glove accuracy, Wi-Fi handoff.
- No hardware-in-the-loop. Testing the implement link properly needs a cart or a
  simulated implement server.
