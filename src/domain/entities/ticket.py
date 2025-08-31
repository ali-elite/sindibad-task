"""
Domain entities for tickets.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from enum import Enum


class TicketStatus(str, Enum):
    """Status of a ticket."""
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"


class ServiceType(str, Enum):
    """Service types for tickets."""
    FLIGHT = "Flight"
    HOTEL = "Hotel"
    VISA = "Visa"
    ESIM = "eSIM"
    WALLET = "Wallet"
    OTHER = "Other"


class Category(str, Enum):
    """Categories for tickets."""
    CANCELLATION = "Cancellation"
    MODIFY = "Modify"
    TOP_UP = "Top Up"
    WITHDRAW = "Withdraw"
    ORDER_RECHECK = "Order Re-Check"
    PRE_PURCHASE = "Pre-Purchase"
    OTHERS = "Others"


@dataclass
class Tag:
    """Represents a tag for a ticket."""
    service_type: Optional[ServiceType] = None
    category: Optional[Category] = None
    confidence: float = 0.0
    method: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_complete(self) -> bool:
        """Check if both service type and category are set."""
        return self.service_type is not None and self.category is not None

    @property
    def is_default_tag(self) -> bool:
        """Check if this is the default 'others-others' tag."""
        return (self.service_type == ServiceType.OTHER and
                self.category == Category.OTHERS)


@dataclass
class Message:
    """Represents a message in a conversation."""
    id: Optional[str] = None
    text: str = ""
    sender: str = ""  # "user" or "bot"
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ticket_id: Optional[str] = None

    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.sender == "user"

    def is_bot_message(self) -> bool:
        """Check if this is a bot message."""
        return self.sender == "bot"


@dataclass
class Ticket:
    """Domain entity for a ticket."""
    ticket_id: str = field(default_factory=lambda: str(uuid4()))
    conversation_id: str = ""
    messages: List[Message] = field(default_factory=list)
    current_tag: Tag = field(default_factory=Tag)
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, message: Message) -> None:
        """Add a message to the ticket."""
        message.ticket_id = self.ticket_id
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def update_tag(self, new_tag: Tag) -> None:
        """Update the ticket's tag."""
        self.current_tag = new_tag
        self.updated_at = datetime.utcnow()

    def get_user_messages(self) -> List[Message]:
        """Get all user messages in the ticket."""
        return [msg for msg in self.messages if msg.is_user_message()]

    def get_latest_user_message(self) -> Optional[Message]:
        """Get the most recent user message."""
        user_messages = self.get_user_messages()
        return user_messages[-1] if user_messages else None

    def should_process_for_tagging(self) -> bool:
        """Check if ticket should be processed for tagging."""
        return (self.status == TicketStatus.OPEN and
                len(self.get_user_messages()) > 0)

    def get_combined_text(self) -> str:
        """Get combined text of all user messages."""
        user_messages = self.get_user_messages()
        return " ".join(msg.text for msg in user_messages)


@dataclass
class Conversation:
    """Represents a conversation with multiple messages."""
    conversation_id: str
    messages: List[Message] = field(default_factory=list)
    ticket: Optional[Ticket] = None

    def add_message(self, message: Message) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def get_user_messages(self) -> List[Message]:
        """Get all user messages in the conversation."""
        return [msg for msg in self.messages if msg.is_user_message()]

    def get_combined_text(self) -> str:
        """Get combined text of all user messages."""
        user_messages = self.get_user_messages()
        return " ".join(msg.text for msg in user_messages)
