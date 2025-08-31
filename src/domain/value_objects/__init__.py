"""
Domain value objects.
"""

from .confidence import ConfidenceScore
from .tagging_result import TaggingResult

__all__ = [
    "ConfidenceScore",
    "TaggingResult",
]
