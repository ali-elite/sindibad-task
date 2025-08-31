"""
Value object for tagging results.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..entities.ticket import ServiceType, Category, Tag


@dataclass(frozen=True)
class TaggingResult:
    """Value object representing the result of a tagging operation."""
    service_type: Optional[ServiceType]
    category: Optional[Category]
    confidence_score: float
    method_used: str
    reasoning: str = ""
    key_phrases: List[str] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = None

    def __post_init__(self):
        """Validate tagging result."""
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")

    def to_tag(self) -> Tag:
        """Convert to a Tag entity."""
        from ..entities.ticket import Tag
        return Tag(
            service_type=self.service_type,
            category=self.category,
            confidence=self.confidence_score,
            method=self.method_used,
            timestamp=self.timestamp or datetime.utcnow()
        )

    @property
    def is_successful(self) -> bool:
        """Check if tagging was successful."""
        return self.service_type is not None or self.category is not None

    @property
    def is_complete(self) -> bool:
        """Check if both service type and category are identified."""
        return self.service_type is not None and self.category is not None

    @property
    def confidence_level(self) -> str:
        """Get confidence level as string."""
        if self.confidence_score >= 0.8:
            return "high"
        elif self.confidence_score >= 0.6:
            return "medium"
        else:
            return "low"

    def __str__(self) -> str:
        """String representation."""
        service = self.service_type.value if self.service_type else "None"
        category = self.category.value if self.category else "None"
        return f"TaggingResult(service={service}, category={category}, confidence={self.confidence_score:.2f})"
