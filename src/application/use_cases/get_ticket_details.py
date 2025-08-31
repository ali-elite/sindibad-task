"""
Use case for getting ticket details.
"""

from typing import Optional, Dict, Any
from ...domain.entities.ticket import Ticket
from ...application.services.ticket_service import TicketService


class GetTicketDetailsUseCase:
    """Use case for retrieving ticket details."""

    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service

    async def execute(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific ticket.

        Args:
            ticket_id: The ticket ID to retrieve

        Returns:
            Dictionary with ticket details or None if not found
        """
        ticket = await self.ticket_service.get_ticket(ticket_id)

        if not ticket:
            return None

        return {
            "ticket_id": ticket.ticket_id,
            "conversation_id": ticket.conversation_id,
            "status": ticket.status.value,
            "current_tag": {
                "service_type": ticket.current_tag.service_type.value if ticket.current_tag.service_type else None,
                "category": ticket.current_tag.category.value if ticket.current_tag.category else None,
                "confidence": ticket.current_tag.confidence,
                "method": ticket.current_tag.method,
                "timestamp": ticket.current_tag.timestamp.isoformat()
            },
            "messages": [
                {
                    "id": msg.id,
                    "text": msg.text,
                    "sender": msg.sender,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in ticket.messages
            ],
            "message_count": len(ticket.messages),
            "user_message_count": len(ticket.get_user_messages()),
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat()
        }
