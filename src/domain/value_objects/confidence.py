"""
Value object for confidence scores.
"""

from dataclasses import dataclass
from typing import Dict, Any
from enum import Enum


class ConfidenceLevel(str, Enum):
    """Confidence levels for tagging."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class ConfidenceScore:
    """Value object representing a confidence score."""
    value: float
    method: str = ""
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Validate confidence score."""
        if not (0.0 <= self.value <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")

    @property
    def level(self) -> ConfidenceLevel:
        """Get the confidence level."""
        if self.value >= 0.8:
            return ConfidenceLevel.HIGH
        elif self.value >= 0.6:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    @property
    def is_high_confidence(self) -> bool:
        """Check if confidence is high."""
        return self.level == ConfidenceLevel.HIGH

    @property
    def is_medium_confidence(self) -> bool:
        """Check if confidence is medium."""
        return self.level == ConfidenceLevel.MEDIUM

    @property
    def is_low_confidence(self) -> bool:
        """Check if confidence is low."""
        return self.level == ConfidenceLevel.LOW

    def __str__(self) -> str:
        """String representation."""
        return f"{self.value:.2f} ({self.level.value})"
