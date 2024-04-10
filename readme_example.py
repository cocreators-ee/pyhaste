import time
from random import uniform

from pyhaste import measure, report, Analyzer


def prepare_task():
    time.sleep(0.1)


def find_items():
    with measure("find_items"):
        return [1, 2, 3]


def process_item(item):
    with measure("process_item"):
        time.sleep(item * 0.1)


with measure("task"):
    with measure("prepare"):
        prepare_task()

    for item in find_items():
        process_item(item)

time.sleep(0.01)
report()

for item in [1, 2, 3]:
    analyzer = Analyzer()
    with analyzer.measure(f"process_item({item})"):
        with analyzer.measure("db.find"):
            time.sleep(uniform(0.04, 0.06) * item)
        with analyzer.measure("calculate"):
            time.sleep(uniform(0.1, 0.15) * item)
        with analyzer.measure("save"):
            time.sleep(uniform(0.05, 0.075) * item)
    time.sleep(uniform(0.01, 0.025) * item)
    analyzer.report()
