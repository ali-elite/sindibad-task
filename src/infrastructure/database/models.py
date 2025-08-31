"""
SQLAlchemy models for database persistence.
"""

from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import datetime

from ...domain.entities.ticket import TicketStatus, ServiceType, Category


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class TicketModel(Base):
    """SQLAlchemy model for Ticket entity."""
    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    conversation_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    service_type: Mapped[Optional[str]] = mapped_column(SQLEnum(ServiceType), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(SQLEnum(Category), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    method: Mapped[str] = mapped_column(String(50), default="")
    status: Mapped[str] = mapped_column(SQLEnum(TicketStatus), nullable=False, default=TicketStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship to messages
    messages: Mapped[List["MessageModel"]] = relationship("MessageModel", back_populates="ticket", cascade="all, delete-orphan")

    def to_domain_entity(self):
        """Convert to domain entity."""
        from ...domain.entities.ticket import Ticket, Tag, Message

        # Create tag from database fields
        tag = Tag(
            service_type=ServiceType(self.service_type) if self.service_type else None,
            category=Category(self.category) if self.category else None,
            confidence=self.confidence,
            method=self.method,
            timestamp=self.created_at
        )

        # Create messages
        messages = [msg.to_domain_entity() for msg in self.messages]

        # Create ticket
        ticket = Ticket(
            ticket_id=self.ticket_id,
            conversation_id=self.conversation_id,
            messages=messages,
            current_tag=tag,
            status=TicketStatus(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at
        )

        return ticket

    @classmethod
    def from_domain_entity(cls, ticket):
        """Create from domain entity."""
        return cls(
            ticket_id=ticket.ticket_id,
            conversation_id=ticket.conversation_id,
            service_type=ticket.current_tag.service_type.value if ticket.current_tag.service_type else None,
            category=ticket.current_tag.category.value if ticket.current_tag.category else None,
            confidence=ticket.current_tag.confidence,
            method=ticket.current_tag.method,
            status=ticket.status.value,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )


class MessageModel(Base):
    """SQLAlchemy model for Message entity."""
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticket_id: Mapped[str] = mapped_column(String(36), ForeignKey("tickets.ticket_id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    sender: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Relationship to ticket
    ticket: Mapped["TicketModel"] = relationship("TicketModel", back_populates="messages")

    def to_domain_entity(self):
        """Convert to domain entity."""
        from ...domain.entities.ticket import Message

        return Message(
            id=str(self.id),
            text=self.text,
            sender=self.sender,
            timestamp=self.timestamp,
            ticket_id=self.ticket_id
        )

    @classmethod
    def from_domain_entity(cls, message):
        """Create from domain entity."""
        return cls(
            id=int(message.id) if message.id else None,
            ticket_id=message.ticket_id,
            text=message.text,
            sender=message.sender,
            timestamp=message.timestamp
        )
