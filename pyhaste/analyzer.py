from contextlib import contextmanager
from functools import wraps
from time import perf_counter
from typing import Iterable, Tuple

from rich.console import Console
from rich.table import Table

Item = Tuple[str, float]
console = Console()
SEP = " -> "


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
    counters: dict[str, int]
    timers: dict[str, float]
    total_time: float
    nested: list[str]

    def __init__(self):
        self.counters = {}
        self.timers = {}
        self.total_time = 0.0
        self.start_time = None
        self.nested = []

    @contextmanager
    def measure(self, name):
        start = perf_counter()
        if not self.start_time:
            self.start_time = start

        self.nested.append(name)
        key = SEP.join(self.nested)

        try:
            yield
        finally:
            self.nested.pop()

            elapsed = perf_counter() - start
            self.counters[key] = 1 + self.counters.get(key, 0.0)
            self.timers[key] = elapsed + self.timers.get(key, 0.0)
            if not self.nested:
                self.total_time += elapsed

    def measure_wrap(self, name):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                with self.measure(name):
                    return f(*args, **kwargs)

            return wrapper

        return decorator

    def get_parent_pct(self, name, elapsed):
        parts = name.split(SEP)
        if len(parts) == 1:
            return ""

        parent_name = SEP.join(parts[:-1])
        parent_total = self.timers[parent_name]

        pct = (elapsed / parent_total) * 100
        return f"{pct:.2f}%"

    def report(self):
        total_elapsed = perf_counter() - self.start_time
        self.timers["Unmeasured"] = total_elapsed - self.total_time
        self.total_time += self.timers["Unmeasured"]

        tbl = Table()
        tbl.add_column("Name", style="bright_green")
        tbl.add_column("Time", style="bright_magenta", justify="right", no_wrap=True)
        tbl.add_column("Tot %", style="bright_blue", justify="right", no_wrap=True)
        tbl.add_column("Rel %", style="bright_yellow", justify="right", no_wrap=True)
        tbl.add_column("Calls", style="cyan", justify="right", no_wrap=True)
        tbl.add_column("Per call", style="bright_magenta", justify="right", no_wrap=True)

        for name, elapsed in sort_items(self.timers.items()):
            pct = (elapsed / self.total_time) * 100
            count = ""
            per_call = ""
            if name in self.counters:
                count = f"{self.counters[name]:,.0f}"
                per_call = format_elapsed(elapsed / self.counters[name])
            tbl.add_row(
                " [blue]›[/blue]".join(name.split(SEP)),
                format_elapsed(elapsed),
                f"{pct:.2f}%",
                self.get_parent_pct(name, elapsed),
                count,
                per_call,
            )

        tbl.add_section()
        tbl.add_row("Total", format_elapsed(self.total_time), "100%", "", "")

        console.print("")
        console.rule("[bold red]PyHaste report", style="green")
        console.print("")
        console.print(tbl)
