"""
Application service for ticket tagging with two-layer approach.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from ...domain.entities.ticket import Ticket, Tag, ServiceType, Category, Message
from ...domain.value_objects.tagging_result import TaggingResult
from ...infrastructure.external_services.keyword_tagger import KeywordTaggingEngine
from ...infrastructure.external_services.agentic_tagger import AgenticTaggingEngine


class TaggingService:
    """
    Application service that orchestrates the two-layer tagging approach:

    1. Keywords Layer: Fast, rule-based tagging using keyword matching
    2. Agentic Layer: Intelligent tagging using AI agents for complex cases
    """

    def __init__(self):
        self.keyword_engine = KeywordTaggingEngine()
        self.agentic_engine = AgenticTaggingEngine()

    async def tag_ticket(self, ticket: Ticket) -> TaggingResult:
        """
        Tag a ticket using the two-layer approach.

        Layer 1: Keywords - Fast initial tagging
        Layer 2: Agentic - Intelligent refinement based on conversation context
        """
        # Get user messages for analysis
        user_messages = ticket.get_user_messages()
        if not user_messages:
            return self._create_default_result("no_user_messages")

        combined_text = ticket.get_combined_text()

        # Layer 1: Keywords-based tagging
        keyword_result = self.keyword_engine.tag_text(combined_text)

        # If keyword layer found a match with high confidence, use it
        if keyword_result.is_successful and keyword_result.confidence_score >= 0.7:
            return keyword_result

        # Layer 2: Agentic tagging for complex cases or low confidence
        if len(user_messages) > 1 or keyword_result.confidence_score < 0.5:
            message_texts = [msg.text for msg in user_messages]
            agentic_result = await self.agentic_engine.tag_conversation(message_texts)

            # Use agentic result if it's more confident or provides different insights
            if (agentic_result.confidence_score > keyword_result.confidence_score or
                agentic_result.is_complete):
                return agentic_result

        # Return keyword result if agentic didn't provide better results
        return keyword_result

    async def update_ticket_tags(self, ticket: Ticket) -> bool:
        """
        Update ticket tags based on new messages and conversation context.

        This is called when new messages are added to an existing ticket.
        """
        # Only update if ticket should be processed
        if not ticket.should_process_for_tagging():
            return False

        # Get new tagging result
        new_result = await self.tag_ticket(ticket)

        # Update ticket tag if result is different or more confident
        current_confidence = ticket.current_tag.confidence
        new_confidence = new_result.confidence_score

        should_update = (
            new_result.is_successful and (
                not ticket.current_tag.is_complete or  # No complete tag yet
                new_confidence > current_confidence or  # More confident
                ticket.current_tag.is_default_tag  # Currently default tag
            )
        )

        if should_update:
            new_tag = new_result.to_tag()
            ticket.update_tag(new_tag)
            return True

        return False

    def _create_default_result(self, reason: str) -> TaggingResult:
        """Create a default 'others-others' tagging result."""
        return TaggingResult(
            service_type=ServiceType.OTHER,
            category=Category.OTHERS,
            confidence_score=0.0,
            method_used="default",
            reasoning=f"Default tag assigned: {reason}",
            key_phrases=[],
            metadata={"reason": reason},
            timestamp=datetime.utcnow()
        )

    def get_tagging_explanation(self, ticket: Ticket) -> Dict[str, Any]:
        """Get detailed explanation of how the ticket was tagged."""
        user_messages = ticket.get_user_messages()
        combined_text = ticket.get_combined_text()

        explanation = {
            "ticket_id": ticket.ticket_id,
            "conversation_id": ticket.conversation_id,
            "current_tag": {
                "service_type": ticket.current_tag.service_type.value if ticket.current_tag.service_type else None,
                "category": ticket.current_tag.category.value if ticket.current_tag.category else None,
                "confidence": ticket.current_tag.confidence,
                "method": ticket.current_tag.method,
                "timestamp": ticket.current_tag.timestamp.isoformat()
            },
            "message_count": len(user_messages),
            "combined_text": combined_text[:500] + "..." if len(combined_text) > 500 else combined_text,
            "layer_analysis": {}
        }

        if combined_text:
            # Get keyword analysis
            keyword_explanation = self.keyword_engine.explain_tagging(combined_text)
            explanation["layer_analysis"]["keywords"] = keyword_explanation

            # Get agentic analysis if available
            try:
                message_texts = [msg.text for msg in user_messages]
                agentic_explanation = self.agentic_engine.explain_tagging(message_texts)
                explanation["layer_analysis"]["agentic"] = agentic_explanation
            except Exception as e:
                explanation["layer_analysis"]["agentic"] = {"error": str(e)}

        return explanation
