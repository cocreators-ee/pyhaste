from typing import Iterable, Tuple

Item = Tuple[str, float]


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
