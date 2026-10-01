# 10-minute demo script

## 0. Open with the limitation (30 seconds — do not skip this)

> "I wanted to bring you something that runs rather than a slide deck. One honest
> caveat up front: BiC is a .NET MAUI native app, and Playwright only drives
> browsers — it physically cannot automate it. Appium with the XCUITest driver is
> the right tool, and that needs Xcode, a signed WebDriverAgent and a cart to talk
> to. So I built a harness of the BiC screens and automated that, and I've written
> out the Appium layer that would point the same suite at the real app."

That paragraph is the interview. It says you know the tooling boundary, you
didn't fake a result, and you already know what the real solution costs.

## 1. Run it (1 min)

```bash
export PYTHONPATH=. && python -m pytest
```
26 passed, ~12 seconds. Then `HEADED=1 python -m pytest tests/test_setup_workflow.py`
so they watch it drive.

## 2. The iPad part (1 min) — `tests/conftest.py`

> "This isn't a desktop browser made narrow. `ipad_context` adopts Playwright's
> iPad Pro 11 descriptor — real user agent, device scale factor, and `has_touch`.
> That's why every page object calls `.tap()` and not `.click()`; a touch context
> has no mouse. And I force landscape, because BiC is landscape-locked —
> `UIRequiresFullScreen`, landscape-only, in its Info.plist."

`test_runs_on_an_emulated_ipad_in_landscape` asserts all three.

## 3. The test design (3 min)

- **`test_begin_operation_is_gated_until_all_three_steps_are_set`** — "This is the
  one I'd care most about. It's a state machine with a point of no return. I assert
  the gate holds after *each* partial step, not just at the end — a test that only
  checks the happy path would pass against a build where the gate never engaged."
- **`test_invalid_ip_is_rejected_and_blocks_save`** — parametrised over four bad
  inputs. "Negative cases are where defects live."
- **`test_implement_server_error_is_surfaced_and_recoverable`** — "Your app
  currently shows *'An error occurred while loading data from implement server'*
  with a Retry. As a tester my question is whether that message tells an operator
  in a field at 6am whether it's the Wi-Fi, the address, or the machine being off.
  So I test that Retry actually recovers, and that one retry on a still-dead link
  doesn't falsely clear the banner."

## 4. CI/CD (2 min) — Actions tab, live

Show a green run. Point at the three triggers:
- **push / PR** — regression gate before merge
- **workflow_dispatch** — press **Run workflow**, pick `connection`, run it in front of them
- **schedule** — `0 11 * * 1-5`

> "Cron in GitHub Actions is always UTC — there's no timezone field. 11 UTC is 5am
> here. Teams get caught by that one."

Then download the artifact to show the HTML report and failure screenshots.

## 5. Close on what it can't do (1 min)

> "What this can't catch: it's emulation, not a physical iPad, so no memory
> pressure, no backgrounding, no Wi-Fi handoff as the rig moves, nothing about
> sunlight or gloves. And no MQTT, protobuf or CAN — that's hardware-in-the-loop
> and it's the part I'd be learning from your team."

## If they ask "did you write this yourself?"

Answer plainly: you designed the test cases and the structure, used AI assistance
to scaffold it quickly, and you can explain and modify any line. Then offer to
change something live — add a parametrised case, flip an assertion, rerun. That
offer settles it, and refusing to make the offer is what looks bad.

## Three questions to ask them

1. "Do your MAUI controls carry `AutomationId`s today? That's the difference
   between a stable XCUITest suite and a flaky one, and it's cheap at build time."
2. "Is there a simulated implement server for testing, or does everything need a
   real cart?"
3. "How do you keep app releases and ECU firmware releases compatible — is there a
   version matrix the test suite checks?"
