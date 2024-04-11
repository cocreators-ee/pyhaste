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
───────────────── PyHaste report ─────────────────

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Name               ┃    Time ┃  Tot % ┃  Rel % ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ task               │ 0.700 s │ 98.58% │        │
│ task ›process_item │ 0.600 s │ 84.49% │ 85.70% │
│ task ›prepare_task │ 0.100 s │ 14.09% │ 14.29% │
│ Unmeasured         │ 0.010 s │  1.42% │        │
│ task ›find_items   │ 0.000 s │  0.00% │  0.00% │
├────────────────────┼─────────┼────────┼────────┤
│ Total              │ 0.710 s │   100% │        │
└────────────────────┴─────────┴────────┴────────┘
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
──────────────────────────────── PyHaste report ────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ process_item(1)                                 │ 0.235 s │ 95.78% │         │
│ process_item(1) ›calculate                      │ 0.121 s │ 49.36% │  51.53% │
│ process_item(1) ›calculate ›guestimate          │ 0.121 s │ 49.36% │ 100.00% │
│ process_item(1) ›calculate ›guestimate ›do_math │ 0.121 s │ 49.35% │  99.99% │
│ process_item(1) ›save                           │ 0.071 s │ 29.19% │  30.48% │
│ process_item(1) ›db.find                        │ 0.042 s │ 17.22% │  17.98% │
│ Unmeasured                                      │ 0.010 s │  4.22% │         │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┤
│ Total                                           │ 0.245 s │   100% │         │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┘

──────────────────────────────── PyHaste report ────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ process_item(2)                                 │ 0.505 s │ 95.09% │         │
│ process_item(2) ›calculate                      │ 0.284 s │ 53.37% │  56.13% │
│ process_item(2) ›calculate ›guestimate          │ 0.284 s │ 53.37% │ 100.00% │
│ process_item(2) ›calculate ›guestimate ›do_math │ 0.284 s │ 53.37% │ 100.00% │
│ process_item(2) ›save                           │ 0.130 s │ 24.45% │  25.71% │
│ process_item(2) ›db.find                        │ 0.092 s │ 17.26% │  18.16% │
│ Unmeasured                                      │ 0.026 s │  4.91% │         │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┤
│ Total                                           │ 0.531 s │   100% │         │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┘

──────────────────────────────── PyHaste report ────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│ process_item(3)                                 │ 0.671 s │ 95.36% │         │
│ process_item(3) ›calculate                      │ 0.330 s │ 46.87% │  49.15% │
│ process_item(3) ›calculate ›guestimate          │ 0.330 s │ 46.87% │ 100.00% │
│ process_item(3) ›calculate ›guestimate ›do_math │ 0.330 s │ 46.87% │ 100.00% │
│ process_item(3) ›save                           │ 0.196 s │ 27.87% │  29.22% │
│ process_item(3) ›db.find                        │ 0.145 s │ 20.62% │  21.62% │
│ Unmeasured                                      │ 0.033 s │  4.64% │         │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┤
│ Total                                           │ 0.704 s │   100% │         │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┘
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
