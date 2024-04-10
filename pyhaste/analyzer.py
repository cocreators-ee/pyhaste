from contextlib import contextmanager
from time import perf_counter
from typing import Iterable, Tuple

from rich.console import Console
from rich.table import Table

Item = Tuple[str, float]
console = Console()


def format_elapsed(elapsed: float) -> str:
    if elapsed < 5:
        decimals = 3
    elif elapsed < 25:
        decimals = 2
    else:
        decimals = 1

    return f"{elapsed:,.{decimals}f} s"


def sort_items(items: Iterable[Item]):
    return sorted(items, key=lambda item: item[1], reverse=True)


class Analyzer:
    counters: dict[str, float]
    total: float
    nested: list[str]

    def __init__(self):
        self.counters = {}
        self.total = 0.0
        self.start_time = None
        self.nested = []

    @contextmanager
    def measure(self, name):
        start = perf_counter()
        if not self.start_time:
            self.start_time = start

        self.nested.append(name)
        counter_name = " [blue]->[/blue] ".join(self.nested)
        yield
        self.nested.pop()

        elapsed = perf_counter() - start
        self.counters[counter_name] = elapsed + self.counters.get(counter_name, 0.0)
        if not self.nested:
            self.total += elapsed

    def report(self):
        total_elapsed = perf_counter() - self.start_time
        self.counters["Unmeasured"] = total_elapsed - self.total
        self.total += self.counters["Unmeasured"]

        tbl = Table()
        tbl.add_column("Name", style="bright_green")
        tbl.add_column("Time", style="bright_magenta", justify="right", no_wrap=True)
        tbl.add_column("%", style="bright_blue", justify="right", no_wrap=True)

        items = self.counters.items()
        items = sort_items(items)
        for name, elapsed in items:
            pct = (elapsed / self.total) * 100
            tbl.add_row(
                name,
                format_elapsed(elapsed),
                f"{pct:.2f}%",
            )
        tbl.add_section()
        tbl.add_row("Total", format_elapsed(self.total), "100%")

        console.print("")
        console.rule("[bold red]PyHaste report", style="green")
        console.print("")
        console.print(tbl)
