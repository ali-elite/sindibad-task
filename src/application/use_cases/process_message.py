"""
Use case for processing incoming messages.
"""

from typing import Dict, Any, List
from ...domain.entities.ticket import Ticket, Message
from ...application.services.ticket_service import TicketService


class ProcessMessageUseCase:
    """Use case for processing webhook messages."""

    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service

    async def execute(self, conversation_id: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process incoming messages from webhook.

        Args:
            conversation_id: The conversation ID
            messages: List of message dictionaries with 'text' and 'sender' keys

        Returns:
            Response dictionary with status and ticket information
        """
        # Convert message dictionaries to Message entities
        message_entities = []
        for msg_data in messages:
            message = Message(
                text=msg_data["text"],
                sender=msg_data["sender"]
            )
            message_entities.append(message)

        # Check if ticket already exists
        existing_ticket = await self.ticket_service.get_ticket_by_conversation(conversation_id)

        if existing_ticket:
            # Add messages to existing ticket
            updated_ticket = await self.ticket_service.add_message_to_ticket(
                conversation_id, message_entities[0]
            )

            return {
                "status": "success",
                "message": "Messages added to existing ticket",
                "ticket_id": updated_ticket.ticket_id if updated_ticket else None,
                "tags_updated": updated_ticket is not None
            }

        else:
            # Create new ticket
            new_ticket = await self.ticket_service.create_ticket(
                conversation_id, message_entities
            )

            return {
                "status": "success",
                "message": "New ticket created",
                "ticket_id": new_ticket.ticket_id,
                "initial_tags": {
                    "service_type": new_ticket.current_tag.service_type.value if new_ticket.current_tag.service_type else None,
                    "category": new_ticket.current_tag.category.value if new_ticket.current_tag.category else None,
                    "confidence": new_ticket.current_tag.confidence
                }
            }
