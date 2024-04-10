import time

from pyhaste import Analyzer


def test_analyzer():
    analyzer = Analyzer()
    with analyzer.measure("start"):
        time.sleep(0.01)
    time.sleep(0.01)
    analyzer.report()
    assert analyzer.counters["start"] >= 0.01
    assert analyzer.counters["Unmeasured"] >= 0.01
    assert analyzer.counters["Unmeasured"] <= 0.02
