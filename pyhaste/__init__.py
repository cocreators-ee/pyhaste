from pyhaste.analyzer import Analyzer

_ANALYZER = Analyzer()

measure = _ANALYZER.measure
report = _ANALYZER.report

__all__ = [
    "Analyzer",
    "measure",
    "report",
]
