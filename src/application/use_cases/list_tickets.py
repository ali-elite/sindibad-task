"""
Use case for listing tickets.
"""

from typing import List, Dict, Any
from ...application.services.ticket_service import TicketService


class ListTicketsUseCase:
    """Use case for listing tickets with filtering and pagination."""

    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service

    async def execute(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        List tickets with pagination.

        Args:
            limit: Maximum number of tickets to return
            offset: Number of tickets to skip

        Returns:
            Dictionary with tickets list and metadata
        """
        tickets = await self.ticket_service.get_all_tickets(limit=limit, offset=offset)

        ticket_summaries = []
        for ticket in tickets:
            summary = {
                "ticket_id": ticket.ticket_id,
                "conversation_id": ticket.conversation_id,
                "status": ticket.status.value,
                "service_type": ticket.current_tag.service_type.value if ticket.current_tag.service_type else None,
                "category": ticket.current_tag.category.value if ticket.current_tag.category else None,
                "confidence": ticket.current_tag.confidence,
                "message_count": len(ticket.messages),
                "user_message_count": len(ticket.get_user_messages()),
                "created_at": ticket.created_at.isoformat(),
                "updated_at": ticket.updated_at.isoformat(),
                "latest_message": ticket.get_latest_user_message().text[:100] + "..." if ticket.get_latest_user_message() else ""
            }
            ticket_summaries.append(summary)

        return {
            "tickets": ticket_summaries,
            "total": len(ticket_summaries),
            "limit": limit,
            "offset": offset
        }
