"""
PRIMA SKOS Monitor

A Python package for monitoring changes in the PRIMA SKOS vocabulary
hosted on SKOSMOS.
"""

import sys
from pathlib import Path

# Automatically add monitor_utils to Python path if not already there
# This allows running without PYTHONPATH=monitor_utils
_init_file = Path(__file__).resolve()
_monitor_utils_dir = _init_file.parent.parent
if str(_monitor_utils_dir) not in sys.path:
    sys.path.insert(0, str(_monitor_utils_dir))

__version__ = "0.1.0"

from prima_skos_monitor.downloader import download_skos
from prima_skos_monitor.analyzer import parse_skos, SKOSConcept
from prima_skos_monitor.comparator import compare_versions, ChangeReport
from prima_skos_monitor.reporter import generate_report

__all__ = [
    "download_skos",
    "parse_skos",
    "SKOSConcept",
    "compare_versions",
    "ChangeReport",
    "generate_report",
]

