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

## Normal usage

To measure your code, `pyhaste` exports a `measure` context manager, give it a name as an argument. Alternatively wrap functions in `measure_wrap` with the name as an argument. Once you want a report call `report` from `pyhaste`.

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
────────────────────────── PyHaste report ───────────────────────────

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Name               ┃    Time ┃  Tot % ┃  Rel % ┃ Calls ┃ Per call ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ task               │ 0.700 s │ 98.58% │        │     1 │  0.700 s │
│ task ›process_item │ 0.600 s │ 84.49% │ 85.70% │     3 │  0.200 s │
│ task ›prepare_task │ 0.100 s │ 14.09% │ 14.29% │     1 │  0.100 s │
│ Unmeasured         │ 0.010 s │  1.42% │        │       │          │
│ task ›find_items   │ 0.000 s │  0.00% │  0.00% │     1 │  0.000 s │
├────────────────────┼─────────┼────────┼────────┼───────┼──────────┤
│ Total              │ 0.710 s │   100% │        │       │          │
└────────────────────┴─────────┴────────┴────────┴───────┴──────────┘
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
────────────────────────────────────────── PyHaste report ──────────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃ Per call ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ process_item(1)                                 │ 0.232 s │ 92.26% │         │     1 │  0.232 s │
│ process_item(1) ›calculate                      │ 0.122 s │ 48.38% │  52.44% │     1 │  0.122 s │
│ process_item(1) ›calculate ›guestimate          │ 0.122 s │ 48.38% │ 100.00% │     1 │  0.122 s │
│ process_item(1) ›calculate ›guestimate ›do_math │ 0.122 s │ 48.37% │  99.99% │     1 │  0.122 s │
│ process_item(1) ›save                           │ 0.058 s │ 23.23% │  25.18% │     1 │  0.058 s │
│ process_item(1) ›db.find                        │ 0.052 s │ 20.64% │  22.37% │     1 │  0.052 s │
│ Unmeasured                                      │ 0.019 s │  7.74% │         │       │          │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┼──────────┤
│ Total                                           │ 0.251 s │   100% │         │       │          │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┴──────────┘

────────────────────────────────────────── PyHaste report ──────────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃ Per call ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ process_item(2)                                 │ 0.511 s │ 94.66% │         │     1 │  0.511 s │
│ process_item(2) ›calculate                      │ 0.288 s │ 53.38% │  56.40% │     1 │  0.288 s │
│ process_item(2) ›calculate ›guestimate          │ 0.288 s │ 53.38% │ 100.00% │     1 │  0.288 s │
│ process_item(2) ›calculate ›guestimate ›do_math │ 0.288 s │ 53.38% │  99.99% │     1 │  0.288 s │
│ process_item(2) ›save                           │ 0.125 s │ 23.10% │  24.41% │     1 │  0.125 s │
│ process_item(2) ›db.find                        │ 0.098 s │ 18.16% │  19.19% │     1 │  0.098 s │
│ Unmeasured                                      │ 0.029 s │  5.34% │         │       │          │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┼──────────┤
│ Total                                           │ 0.540 s │   100% │         │       │          │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┴──────────┘

────────────────────────────────────────── PyHaste report ──────────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Name                                            ┃    Time ┃  Tot % ┃   Rel % ┃ Calls ┃ Per call ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ process_item(3)                                 │ 0.749 s │ 93.21% │         │     1 │  0.749 s │
│ process_item(3) ›calculate                      │ 0.368 s │ 45.84% │  49.18% │     1 │  0.368 s │
│ process_item(3) ›calculate ›guestimate          │ 0.368 s │ 45.84% │ 100.00% │     1 │  0.368 s │
│ process_item(3) ›calculate ›guestimate ›do_math │ 0.368 s │ 45.84% │ 100.00% │     1 │  0.368 s │
│ process_item(3) ›save                           │ 0.217 s │ 27.07% │  29.04% │     1 │  0.217 s │
│ process_item(3) ›db.find                        │ 0.163 s │ 20.29% │  21.77% │     1 │  0.163 s │
│ Unmeasured                                      │ 0.055 s │  6.79% │         │       │          │
├─────────────────────────────────────────────────┼─────────┼────────┼─────────┼───────┼──────────┤
│ Total                                           │ 0.803 s │   100% │         │       │          │
└─────────────────────────────────────────────────┴─────────┴────────┴─────────┴───────┴──────────┘
```

## Async usage and FastAPI example

Async Python causes some problems for following the stack, so we can't create these nested call stacks and relative calculations automatically. If you're ok with just making sure your names have the necessary degree of identification in some other way, you can use the async version by importing from `pyhaste.async_analyzer`. There's also an additional `measure_wrap_async`.

See [pyhaste_async_demo.py](./pyhaste_async_demo.py) and the [FastAPI demo](./fastapi_demo/pyhaste_fastapi_demo.py) for usage examples.

If you've got good ideas on how we can reliably track the call stack context in `async` Python code please do share 🙂

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
