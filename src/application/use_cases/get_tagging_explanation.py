"""
Use case for getting tagging explanations.
"""

from typing import Optional, Dict, Any
from ...application.services.ticket_service import TicketService
from ...application.services.tagging_service import TaggingService


class GetTaggingExplanationUseCase:
    """Use case for getting detailed tagging explanations."""

    def __init__(self, ticket_service: TicketService, tagging_service: TaggingService):
        self.ticket_service = ticket_service
        self.tagging_service = tagging_service

    async def execute(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed explanation of how a ticket was tagged.

        Args:
            ticket_id: The ticket ID to explain

        Returns:
            Dictionary with tagging explanation or None if ticket not found
        """
        ticket = await self.ticket_service.get_ticket(ticket_id)

        if not ticket:
            return None

        # Get detailed explanation from tagging service
        explanation = self.tagging_service.get_tagging_explanation(ticket)

        return explanation
