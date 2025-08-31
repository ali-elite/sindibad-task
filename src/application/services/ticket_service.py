"""
Application service for ticket management.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from ...domain.entities.ticket import Ticket, Message, TicketStatus, Tag
from ...domain.value_objects.tagging_result import TaggingResult
from ...infrastructure.database.ticket_repository import TicketRepository
from .tagging_service import TaggingService
from .bot_service import BotService


class TicketService:
    """Application service for managing tickets and their lifecycle."""

    def __init__(self):
        self.repository = TicketRepository()
        self.tagging_service = TaggingService()
        self.bot_service = BotService()

    async def create_ticket(self, conversation_id: str, initial_messages: List[Message]) -> Ticket:
        """Create a new ticket from conversation messages."""
        # Create ticket
        ticket = Ticket(conversation_id=conversation_id)

        # Add initial messages
        for message in initial_messages:
            ticket.add_message(message)

        # Tag the ticket
        tagging_result = await self.tagging_service.tag_ticket(ticket)
        ticket.update_tag(tagging_result.to_tag())

        # Save to repository
        await self.repository.save(ticket)

        # Generate bot response if appropriate
        if self._should_generate_bot_response(ticket):
            await self.bot_service.generate_response(ticket)

        return ticket

    async def add_message_to_ticket(self, conversation_id: str, message: Message) -> Optional[Ticket]:
        """Add a message to an existing ticket."""
        # Get existing ticket
        ticket = await self.repository.get_by_conversation_id(conversation_id)
        if not ticket:
            return None

        # Add message
        ticket.add_message(message)

        # Update tags if needed
        updated = await self.tagging_service.update_ticket_tags(ticket)
        if updated:
            await self.repository.save(ticket)

        # Generate bot response if appropriate
        if self._should_generate_bot_response(ticket):
            await self.bot_service.generate_response(ticket)

        return ticket

    async def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get a ticket by ID."""
        return await self.repository.get_by_id(ticket_id)

    async def get_ticket_by_conversation(self, conversation_id: str) -> Optional[Ticket]:
        """Get a ticket by conversation ID."""
        return await self.repository.get_by_conversation_id(conversation_id)

    async def get_all_tickets(self, limit: int = 100, offset: int = 0) -> List[Ticket]:
        """Get all tickets with pagination."""
        return await self.repository.get_all(limit=limit, offset=offset)

    async def update_ticket_status(self, ticket_id: str, status: TicketStatus) -> Optional[Ticket]:
        """Update ticket status."""
        ticket = await self.repository.get_by_id(ticket_id)
        if not ticket:
            return None

        ticket.status = status
        ticket.updated_at = datetime.utcnow()
        await self.repository.save(ticket)
        return ticket

    async def get_ticket_stats(self) -> Dict[str, Any]:
        """Get ticket statistics."""
        return await self.repository.get_stats()

    def _should_generate_bot_response(self, ticket: Ticket) -> bool:
        """Determine if a bot response should be generated."""
        # Generate for new tickets or specific categories
        if len(ticket.messages) <= 1:
            return True

        # Generate for immediate action categories
        immediate_categories = ["Cancellation", "Modify", "Top Up", "Withdraw"]
        if ticket.current_tag.category and ticket.current_tag.category.value in immediate_categories:
            return True

        return False

    async def get_corner_case_stats(self) -> Dict[str, Any]:
        """Get comprehensive corner case statistics."""
        return await self.repository.get_corner_case_stats()

    async def get_problematic_tickets(self, limit: int = 20) -> List[Ticket]:
        """Get tickets that represent corner cases."""
        return await self.repository.get_problematic_tickets(limit)

    def _is_corner_case_ticket(self, ticket: Ticket) -> bool:
        """Check if a ticket represents a corner case."""
        # Low confidence (< 50%)
        if ticket.current_tag.confidence < 0.5:
            return True

        # Default fallback tags
        if ticket.current_tag.is_default_tag:
            return True

        # Missing classifications
        if not ticket.current_tag.service_type or not ticket.current_tag.category:
            return True

        # Very short or very long conversations
        user_messages = ticket.get_user_messages()
        if len(user_messages) == 0 or len(user_messages) > 10:
            return True

        # Short message content
        combined_text = ticket.get_combined_text()
        if len(combined_text.strip()) < 10:
            return True

        return False
