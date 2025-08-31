"""
Application service for bot responses.
"""

from typing import Optional
from ...domain.entities.ticket import Ticket, Message
from datetime import datetime


class BotService:
    """Application service for generating bot responses."""

    def __init__(self):
        self.response_templates = self._load_response_templates()

    def _load_response_templates(self) -> dict:
        """Load response templates for different service types and categories."""
        return {
            "Flight": {
                "Modify": "Thanks for reaching out about your flight modification. To help you change your booking, could you please provide your booking reference number or PNR?",
                "Cancellation": "I understand you'd like to cancel your flight booking. Please provide your booking reference so I can check the cancellation policy and process your request.",
                "Order Re-Check": "I'll help you check your flight booking status. Please share your booking reference number or PNR.",
                "default": "I'm here to help with your flight-related inquiry. Could you please provide more details about what you need assistance with?"
            },
            "Hotel": {
                "Modify": "I'd be happy to help modify your hotel reservation. Please provide your booking confirmation number so I can check availability for your requested changes.",
                "Cancellation": "I can assist with canceling your hotel reservation. Please share your booking confirmation number and I'll review the cancellation terms.",
                "Order Re-Check": "Let me check your hotel reservation details. Please provide your booking confirmation number.",
                "default": "I'm here to assist with your hotel booking. What specific help do you need today?"
            },
            "Visa": {
                "Modify": "I can help you modify your visa application. Please provide your application reference number so I can check what changes are possible.",
                "Order Re-Check": "I'll check your visa application status. Please share your application reference number.",
                "default": "I'm here to help with your visa application. What assistance do you need?"
            },
            "eSIM": {
                "Top Up": "I can help you top up your eSIM data plan. Let me check your current balance and available top-up options.",
                "Order Re-Check": "I'll check your eSIM status and data usage. One moment please.",
                "default": "I'm here to assist with your eSIM service. How can I help you today?"
            },
            "Wallet": {
                "Top Up": "I can help you add funds to your wallet. What amount would you like to top up?",
                "Withdraw": "I'll assist you with withdrawing funds from your wallet. Please confirm the amount you'd like to withdraw.",
                "Order Re-Check": "Let me check your wallet balance and recent transactions.",
                "default": "I'm here to help with your wallet services. What do you need assistance with?"
            },
            "Other": {
                "Pre-Purchase": "Thank you for your inquiry! I'm here to help you with information before you make a purchase. What would you like to know?",
                "Others": "I'm here to help! Could you please provide more details about what you need assistance with?",
                "default": "Hello! I'm here to assist you. Could you please let me know what you need help with today?"
            }
        }

    async def generate_response(self, ticket: Ticket) -> Optional[Message]:
        """Generate a bot response for the ticket."""
        if not ticket.should_process_for_tagging():
            return None

        response_text = self._get_response_text(ticket)

        # Create bot message
        bot_message = Message(
            text=response_text,
            sender="bot",
            ticket_id=ticket.ticket_id,
            timestamp=datetime.utcnow()
        )

        # Add to ticket
        ticket.add_message(bot_message)

        # Log the response (would integrate with external logging service)
        self._log_bot_response(ticket, bot_message)

        return bot_message

    def _get_response_text(self, ticket: Ticket) -> str:
        """Get appropriate response text based on ticket tags."""
        service_type = ticket.current_tag.service_type
        category = ticket.current_tag.category

        if service_type:
            service_templates = self.response_templates.get(service_type.value, {})
            if category and category.value in service_templates:
                return service_templates[category.value]
            return service_templates.get("default", self.response_templates["Other"]["default"])

        return self.response_templates["Other"]["default"]

    def _log_bot_response(self, ticket: Ticket, message: Message):
        """Log bot response for monitoring."""
        # In a real implementation, this would send to a logging service
        print(f"[BOT_RESPONSE] Ticket {ticket.ticket_id}: {message.text[:100]}...")

    def should_generate_response(self, ticket: Ticket) -> bool:
        """Determine if a bot response should be generated."""
        # Generate for first user message
        user_messages = ticket.get_user_messages()
        if len(user_messages) <= 1:
            return True

        # Generate for specific categories that need immediate attention
        if ticket.current_tag.category:
            immediate_categories = ["Cancellation", "Modify", "Top Up", "Withdraw"]
            if ticket.current_tag.category.value in immediate_categories:
                return True

        return False
