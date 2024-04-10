import time
from random import uniform

from pyhaste import measure, report


def prepare():
    print(f"Preparing")
    time.sleep(uniform(0.5, 1.5))


def find_items():
    with measure("db.find"):
        print("Finding items")
        time.sleep(uniform(0.1, .3))
        return [1, 2, 3]


def process_item(item: int):
    with measure("process_item"):
        print(f"Processing {item}")
        time.sleep(uniform(0.05, .25))
        return item ** 2


def save_item():
    with measure("db.save"):
        print(f"Saving items")
        time.sleep(uniform(0.01, 0.02))


def do_stuff():
    items = find_items()
    for item in items:
        process_item(item)
    save_item()


if __name__ == "__main__":
    with measure("prepare"):
        prepare()

    time.sleep(uniform(0.1, 0.25))

    elapsed = 0
    while elapsed < 6:
        start = time.perf_counter()

        with measure("do_stuff"):
            do_stuff()

        elapsed += time.perf_counter() - start

    time.sleep(uniform(0.1, 0.25))

    report()
