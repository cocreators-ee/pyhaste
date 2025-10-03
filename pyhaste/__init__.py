from pyhaste.analyzer import Analyzer
from pyhaste.async_analyzer import AsyncAnalyzer

_ANALYZER = Analyzer()

measure = _ANALYZER.measure
measure_wrap = _ANALYZER.measure_wrap
report = _ANALYZER.report

__all__ = [
    "Analyzer",
    "AsyncAnalyzer",
    "measure",
    "measure_wrap",
    "report",
]
