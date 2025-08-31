"""
Use case for updating ticket status.
"""

from typing import Optional, Dict, Any
from ...domain.entities.ticket import TicketStatus
from ...application.services.ticket_service import TicketService


class UpdateTicketStatusUseCase:
    """Use case for updating ticket status."""

    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service

    async def execute(self, ticket_id: str, status: TicketStatus) -> Dict[str, Any]:
        """
        Update the status of a ticket.

        Args:
            ticket_id: The ticket ID to update
            status: The new status

        Returns:
            Dictionary with update result
        """
        updated_ticket = await self.ticket_service.update_ticket_status(ticket_id, status)

        if not updated_ticket:
            return {
                "status": "error",
                "message": "Ticket not found",
                "ticket_id": ticket_id
            }

        return {
            "status": "success",
            "message": f"Ticket status updated to {status.value}",
            "ticket_id": ticket_id,
            "new_status": status.value
        }
