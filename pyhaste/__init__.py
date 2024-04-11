from pyhaste.analyzer import Analyzer

_ANALYZER = Analyzer()

measure = _ANALYZER.measure
measure_wrap = _ANALYZER.measure_wrap
report = _ANALYZER.report

__all__ = [
    "Analyzer",
    "measure",
    "measure_wrap",
    "report",
]
