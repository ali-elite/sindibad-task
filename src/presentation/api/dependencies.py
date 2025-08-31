"""
API dependencies for dependency injection.
"""

from ...application.services.ticket_service import TicketService
from ...application.services.tagging_service import TaggingService


# Global service instances (in production, use proper DI container)
_ticket_service = None
_tagging_service = None


def get_ticket_service() -> TicketService:
    """Get ticket service instance."""
    global _ticket_service
    if _ticket_service is None:
        _ticket_service = TicketService()
    return _ticket_service


def get_tagging_service() -> TaggingService:
    """Get tagging service instance."""
    global _tagging_service
    if _tagging_service is None:
        _tagging_service = TaggingService()
    return _tagging_service
