from contextlib import contextmanager
from functools import wraps
from time import perf_counter

from rich.console import Console
from rich.table import Table

from pyhaste.common import format_elapsed, sort_items

console = Console()


class AsyncAnalyzer:
    counters: dict[str, int]
    timers: dict[str, float]

    def __init__(self):
        self.counters = {}
        self.timers = {}
        self.start_time = perf_counter()

    @contextmanager
    def measure(self, name):
        start = perf_counter()
        if not self.start_time:
            self.start_time = start

        try:
            yield
        finally:
            elapsed = perf_counter() - start
            self.counters[name] = 1 + self.counters.get(name, 0.0)
            self.timers[name] = elapsed + self.timers.get(name, 0.0)

    def measure_wrap(self, name):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                with self.measure(name):
                    return f(*args, **kwargs)

            return wrapper

        return decorator

    def measure_wrap_async(self, name):
        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                with self.measure(name):
                    return await f(*args, **kwargs)

            return wrapper

        return decorator

    def report(self):
        # Largest time is as close to total time we can get
        max_time = max(*self.timers.values())

        tbl = Table()
        tbl.add_column("Name", style="bright_green")
        tbl.add_column("Time", style="bright_magenta", justify="right", no_wrap=True)
        tbl.add_column("Tot %", style="bright_blue", justify="right", no_wrap=True)
        tbl.add_column("Calls", style="cyan", justify="right", no_wrap=True)
        tbl.add_column("Per call", style="bright_magenta", justify="right", no_wrap=True)

        for name, elapsed in sort_items(self.timers.items()):
            pct = (elapsed / max_time) * 100
            count = ""
            per_call = ""
            if name in self.counters:
                count = f"{self.counters[name]:,.0f}"
                per_call = format_elapsed(elapsed / self.counters[name])
            tbl.add_row(
                name,
                format_elapsed(elapsed),
                f"{pct:.2f}%",
                count,
                per_call,
            )

        tbl.add_section()
        tbl.add_row("Max", format_elapsed(max_time), "100%", "", "")

        console.print("")
        console.rule("[bold red]PyHaste report", style="green")
        console.print("")
        console.print(tbl)


_ANALYZER = AsyncAnalyzer()

measure = _ANALYZER.measure
measure_wrap = _ANALYZER.measure_wrap
measure_wrap_async = _ANALYZER.measure_wrap_async
report = _ANALYZER.report
