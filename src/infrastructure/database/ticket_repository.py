"""
Repository for ticket data persistence.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy import select, update, func, case, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime

from ...domain.entities.ticket import Ticket, Message, TicketStatus, ServiceType, Category, Tag
from .database_config import DatabaseConfig
from .models import TicketModel, MessageModel, Base


class TicketRepository:
    """Repository for ticket data operations."""

    def __init__(self):
        self.config = DatabaseConfig()
        self.engine = self.config.create_engine()
        self.session_factory = self.config.create_session_factory(self.engine)

    async def initialize_database(self) -> None:
        """Initialize the database schema."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def save(self, ticket: Ticket) -> None:
        """Save or update a ticket."""
        async with self.session_factory() as session:
            # Check if ticket already exists
            existing = await session.get(TicketModel, ticket.ticket_id)

            if existing:
                # Update existing ticket
                existing.conversation_id = ticket.conversation_id
                existing.service_type = ticket.current_tag.service_type.value if ticket.current_tag.service_type else None
                existing.category = ticket.current_tag.category.value if ticket.current_tag.category else None
                existing.confidence = ticket.current_tag.confidence
                existing.method = ticket.current_tag.method
                existing.status = ticket.status.value
                existing.updated_at = ticket.updated_at

                # Update messages - for simplicity, we'll replace all messages
                # In a production system, you'd want to handle message updates more carefully
                await session.execute(
                    delete(MessageModel).where(MessageModel.ticket_id == ticket.ticket_id)
                )

                for message in ticket.messages:
                    message_model = MessageModel.from_domain_entity(message)
                    session.add(message_model)
            else:
                # Create new ticket
                ticket_model = TicketModel.from_domain_entity(ticket)
                session.add(ticket_model)

                # Add messages
                for message in ticket.messages:
                    message_model = MessageModel.from_domain_entity(message)
                    session.add(message_model)

            await session.commit()

    async def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID."""
        async with self.session_factory() as session:
            stmt = select(TicketModel).options(selectinload(TicketModel.messages)).where(TicketModel.ticket_id == ticket_id)
            result = await session.execute(stmt)
            ticket_model = result.scalar_one_or_none()

            if ticket_model:
                return ticket_model.to_domain_entity()
            return None

    async def get_by_conversation_id(self, conversation_id: str) -> Optional[Ticket]:
        """Get ticket by conversation ID."""
        async with self.session_factory() as session:
            stmt = select(TicketModel).options(selectinload(TicketModel.messages)).where(TicketModel.conversation_id == conversation_id)
            result = await session.execute(stmt)
            ticket_model = result.scalar_one_or_none()

            if ticket_model:
                return ticket_model.to_domain_entity()
            return None

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Ticket]:
        """Get all tickets with pagination."""
        async with self.session_factory() as session:
            stmt = select(TicketModel).options(selectinload(TicketModel.messages)).order_by(TicketModel.created_at.desc()).limit(limit).offset(offset)
            result = await session.execute(stmt)
            ticket_models = result.scalars().all()

            return [ticket_model.to_domain_entity() for ticket_model in ticket_models]

    async def get_stats(self) -> Dict[str, Any]:
        """Get ticket statistics."""
        async with self.session_factory() as session:
            # Total tickets
            total_stmt = select(func.count(TicketModel.ticket_id))
            total_result = await session.execute(total_stmt)
            total_tickets = total_result.scalar()

            # Status distribution
            status_stmt = select(
                TicketModel.status,
                func.count(TicketModel.ticket_id).label('count')
            ).group_by(TicketModel.status)

            status_result = await session.execute(status_stmt)
            status_distribution = {row.status: row.count for row in status_result}

            # Service distribution
            service_stmt = select(
                TicketModel.service_type,
                func.count(TicketModel.ticket_id).label('count')
            ).where(TicketModel.service_type.isnot(None)).group_by(TicketModel.service_type)

            service_result = await session.execute(service_stmt)
            service_distribution = {row.service_type: row.count for row in service_result}

            return {
                "total_tickets": total_tickets,
                "status_distribution": status_distribution,
                "service_distribution": service_distribution
            }

    async def delete(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        async with self.session_factory() as session:
            ticket = await session.get(TicketModel, ticket_id)
            if ticket:
                await session.delete(ticket)
                await session.commit()
                return True
            return False
