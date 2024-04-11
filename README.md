# PyHaste

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/cocreators-ee/pyhaste/publish.yaml)](https://github.com/cocreators-ee/pyhaste/actions/workflows/publish.yaml)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/cocreators-ee/pyhaste/blob/master/.pre-commit-config.yaml)
[![PyPI](https://img.shields.io/pypi/v/pyhaste)](https://pypi.org/project/pyhaste/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyhaste)](https://pypi.org/project/pyhaste/)
[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Python code speed analyzer.

![PyHaste screenshot](https://github.com/cocreators-ee/pyhaste/raw/main/pyhaste.png)

Monitor the performance of your scripts etc. tools and understand where time is spent.

## Installation

It's a Python library, what do you expect?

```bash
pip install pyhaste
# OR
poetry add pyhaste
```

## Usage

To measure your code, `pyhaste` exports a `measure` context manager, give it a name as an argument. Once you want a report call `report` from `pyhaste`.

```python
import time

from pyhaste import measure, report, measure_wrap


@measure_wrap("prepare_task")
def prepare_task():
  time.sleep(0.1)


@measure_wrap("find_items")
def find_items():
  return [1, 2, 3]


@measure_wrap("process_item")
def process_item(item):
  time.sleep(item * 0.1)


with measure("task"):
  prepare_task()

  for item in find_items():
    process_item(item)

time.sleep(0.01)
report()

```

```
───────────────────── PyHaste report ─────────────────────

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ Name               ┃    Time ┃  Tot % ┃  Rel % ┃ Calls ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ task               │ 0.700 s │ 98.58% │        │     1 │
│ task ›process_item │ 0.600 s │ 84.49% │ 85.71% │     3 │
│ task ›prepare_task │ 0.100 s │ 14.08% │ 14.29% │     1 │
│ Unmeasured         │ 0.010 s │  1.42% │        │       │
│ task ›find_items   │ 0.000 s │  0.00% │  0.00% │     1 │
├────────────────────┼─────────┼────────┼────────┼───────┤
│ Total              │ 0.710 s │   100% │        │       │
└────────────────────┴─────────┴────────┴────────┴───────┘
```

In case you need more complex analysis, you might benefit from `pyhaste.Analyzer` and creating your own instances, e.g. for measuring time spent on separate tasks in a longer running job:

```python
import time
from random import uniform
from pyhaste import Analyzer

for item in [1, 2, 3]:
  analyzer = Analyzer()
  with analyzer.measure(f"process_item({item})"):
    with analyzer.measure("db.find"):
      time.sleep(uniform(0.04, 0.06) * item)
    with analyzer.measure("calculate"):
      with analyzer.measure("guestimate"):
        with analyzer.measure("do_math"):
          time.sleep(uniform(0.1, 0.15) * item)
    with analyzer.measure("save"):
      time.sleep(uniform(0.05, 0.075) * item)
  time.sleep(uniform(0.01, 0.025) * item)
  analyzer.report()
```

```
──────────────────────────────────── PyHaste report ────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ process_item(1)                                 │ 0.219 s │ 93.61% │         │     1 │
│ process_item(1) ›calculate                      │ 0.121 s │ 51.69% │  55.22% │     1 │
│ process_item(1) ›calculate ›guestimate          │ 0.121 s │ 51.69% │ 100.00% │     1 │
│ process_item(1) ›calculate ›guestimate ›do_math │ 0.121 s │ 51.69% │  99.99% │     1 │
│ process_item(1) ›save                           │ 0.055 s │ 23.66% │  25.28% │     1 │
│ process_item(1) ›db.find                        │ 0.043 s │ 18.24% │  19.49% │     1 │
│ Unmeasured                                      │ 0.015 s │  6.39% │         │       │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┤
│ Total                                           │ 0.234 s │   100% │         │       │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┘

──────────────────────────────────── PyHaste report ────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ process_item(2)                                 │ 0.474 s │ 92.57% │         │     1 │
│ process_item(2) ›calculate                      │ 0.211 s │ 41.26% │  44.57% │     1 │
│ process_item(2) ›calculate ›guestimate          │ 0.211 s │ 41.26% │ 100.00% │     1 │
│ process_item(2) ›calculate ›guestimate ›do_math │ 0.211 s │ 41.26% │  99.99% │     1 │
│ process_item(2) ›save                           │ 0.146 s │ 28.44% │  30.72% │     1 │
│ process_item(2) ›db.find                        │ 0.117 s │ 22.86% │  24.70% │     1 │
│ Unmeasured                                      │ 0.038 s │  7.43% │         │       │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┤
│ Total                                           │ 0.512 s │   100% │         │       │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┘

──────────────────────────────────── PyHaste report ────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ process_item(3)                                 │ 0.719 s │ 91.02% │         │     1 │
│ process_item(3) ›calculate                      │ 0.374 s │ 47.32% │  51.99% │     1 │
│ process_item(3) ›calculate ›guestimate          │ 0.374 s │ 47.32% │ 100.00% │     1 │
│ process_item(3) ›calculate ›guestimate ›do_math │ 0.374 s │ 47.32% │  99.99% │     1 │
│ process_item(3) ›save                           │ 0.190 s │ 23.99% │  26.36% │     1 │
│ process_item(3) ›db.find                        │ 0.156 s │ 19.70% │  21.64% │     1 │
│ Unmeasured                                      │ 0.071 s │  8.98% │         │       │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┤
│ Total                                           │ 0.790 s │   100% │         │       │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┘
```

## Development

Issues and PRs are welcome!

Please open an issue first to discuss the idea before sending a PR so that you know if it would be wanted or needs
re-thinking or if you should just make a fork for yourself.

For local development, make sure you install [pre-commit](https://pre-commit.com/#install), then run:

```bash
pre-commit install
poetry install
poetry run ptw .
poetry run python example.py

cd fastapi_example
poetry run python example.py
```

## License

The code is released under the BSD 3-Clause license. Details in the [LICENSE.md](./LICENSE.md) file.

# Financial support

This project has been made possible thanks to [Cocreators](https://cocreators.ee) and [Lietu](https://lietu.net). You
can help us continue our open source work by supporting us
on [Buy me a coffee](https://www.buymeacoffee.com/cocreators).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cocreators)
