# Terminal commands — the shell side of this POC

Every command here was used to build, run or ship this suite. If they ask what
Linux/shell experience you have, walk this list rather than claiming a level.

## Project setup

```bash
mkdir -p bic-automation-poc/{app,pages,tests,appium,.github/workflows}
cd bic-automation-poc

python3 -m venv .venv            # isolate dependencies
source .venv/bin/activate        # (Windows: .venv\Scripts\activate)

pip install -r requirements.txt
python -m playwright install chromium    # downloads the browser binary
```

## Running the suite

```bash
export PYTHONPATH=.               # so `from pages...` resolves from the repo root

python -m pytest                              # everything
python -m pytest -v                           # one line per test
python -m pytest tests/test_navigation.py     # one module
python -m pytest -k "invalid_ip"              # by name substring
python -m pytest -m smoke                     # by marker
python -m pytest --lf                         # rerun last failures only
HEADED=1 python -m pytest                     # watch the browser drive itself
python -m pytest -n 4                         # parallel (needs pytest-xdist)

./run.sh                                      # wrapper: sets PYTHONPATH, makes reports/, runs
```

## Inspecting results — standard Unix text handling

```bash
ls -la reports/
open reports/report.html                 # macOS   (Linux: xdg-open)

grep -c "PASSED" reports/junit.xml
grep -o 'tests="[0-9]*"' reports/junit.xml
grep -rn "192.168.200.1" pages/ tests/   # where is the implement IP referenced?
find . -name "*.py" | wc -l              # file count
wc -l pages/*.py tests/*.py              # lines per module
sed -n '1,30p' tests/conftest.py         # print a range without opening an editor
chmod +x run.sh                          # make the wrapper executable
tail -f reports/pytest.log               # follow a long run
```

## Git and GitHub

```bash
git init
git branch -M main
git add .
git commit -m "BiC UI regression suite: Playwright + pytest, iPad emulation"

git remote add origin https://github.com/<you>/bic-automation-poc.git
git push -u origin main

git checkout -b feature/connection-validation
git add tests/test_connection_settings.py
git commit -m "Add port range validation cases"
git push -u origin feature/connection-validation
# then open a Pull Request on GitHub -> CI runs on the PR before merge

git log --oneline -10
git status
git diff HEAD~1
```

## GitHub Actions

```bash
gh workflow list                                  # requires the gh CLI
gh workflow run "BiC UI Regression" -f suite=connection
gh run list --workflow="BiC UI Regression"
gh run watch
gh run download <run-id>                          # pull the report artifact
```

Without the CLI: **Actions** tab → *BiC UI Regression* → **Run workflow** → pick a
suite → **Run**. That button exists because of `workflow_dispatch` in `ci.yml`.

## Cron — explain the schedule line

```
on:
  schedule:
    - cron: "0 11 * * 1-5"
             │ │  │ │  └── Mon–Fri
             │ │  │ └───── every month
             │ │  └─────── every day of month
             │ └────────── hour 11 UTC  = 05:00 Saskatchewan (CST, UTC-6)
             └──────────── minute 0
```

GitHub Actions cron is **always UTC** — there is no timezone field. That is a real
gotcha worth mentioning: a team that writes `0 5 * * *` expecting 5am local gets
11pm local instead.
