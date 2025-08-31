"""
Agentic tagging engine (Layer 2) - Multi-Agent System using OpenAI Agents SDK.
"""

import os
import asyncio
import json
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from agents import Agent, Runner, function_tool, SQLiteSession

from ...domain.entities.ticket import ServiceType, Category
from ...domain.value_objects.tagging_result import TaggingResult

logger = logging.getLogger(__name__)

# Environment variable validation
def validate_openai_config():
    """Validate OpenAI configuration and provide helpful messages."""
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        logger.warning("OPENAI_API_KEY environment variable is not set. AI features will use fallback mode.")
        return False

    if api_key in ["sk-your-openai-api-key-here", "sk-mock-api-key-for-development-replace-with-real-key"]:
        logger.warning("OPENAI_API_KEY is set to placeholder value. AI features will use fallback mode.")
        logger.info("To enable AI features, set OPENAI_API_KEY to a valid OpenAI API key in your .env file")
        return False

    if not api_key.startswith("sk-"):
        logger.warning("OPENAI_API_KEY does not appear to be a valid OpenAI API key format. AI features will use fallback mode.")
        return False

    logger.info("OpenAI API key validated successfully. AI features are enabled.")
    return True

# Validate configuration on module import
OPENAI_AVAILABLE = validate_openai_config()


# Pure LLM-based system - no tools needed


class AgenticTaggingEngine:
    """
    Intelligent agentic tagging engine using OpenAI Agents SDK.
    Uses a single AI agent to dynamically analyze conversation content and determine service type and category.
    """

    def __init__(self, session_db_path: Optional[str] = None):
        # Use environment variable for session database path
        self.session_db_path = session_db_path or os.getenv("SESSION_DB_PATH", "agent_sessions.db")

        self.metrics = {
            "total_taggings": 0,
            "successful_taggings": 0,
            "average_confidence": 0.0,
            "error_count": 0,
            "last_reset": datetime.utcnow()
        }

        # Initialize the AI agent
        self._setup_agent()

    def _setup_agent(self):
        """Set up the AI agent for conversation analysis."""

        self.ai_agent = Agent(
            name="Conversation Analysis Agent",
            instructions="""
            You are an intelligent AI agent specialized in analyzing customer service conversations for a travel and services company.

            Your task is to dynamically analyze the conversation content and determine:
            1. **Service Type**: Which service the customer is inquiring about
               - FLIGHT: Flight bookings, cancellations, changes, status checks
               - HOTEL: Hotel reservations, check-in/out, modifications
               - VISA: Visa applications, status, requirements, documents
               - ESIM: Mobile data plans, connectivity, SIM cards, roaming
               - WALLET: Payment services, balances, top-ups, withdrawals
               - OTHER: General inquiries or when service is unclear

            2. **Category**: What action the customer wants to perform
               - CANCELLATION: Cancel services, get refunds, terminate bookings
               - MODIFY: Change existing bookings/reservations, updates, alterations
               - TOP_UP: Add funds, recharge wallet, load money, deposits
               - WITHDRAW: Remove funds, cash out, withdrawals, transfers
               - ORDER_RECHECK: Check status, verify bookings, confirm details, track orders
               - PRE_PURCHASE: Get information before buying, guidance, how-to questions
               - OTHERS: General inquiries, miscellaneous requests, or unclear actions

            Use your natural language understanding to analyze the conversation. Be intelligent and context-aware:
            - Look for implied meanings and understand customer intent
            - Consider the overall context of the conversation
            - Don't rely on specific keywords - understand the semantic meaning
            - If something is ambiguous, use your best judgment or classify as OTHER

            Always provide:
            - Clear reasoning for your classification
            - Confidence score (0.0 to 1.0) based on how clear the conversation is
            - Key phrases that support your decision
            - Any ambiguities or uncertainties you encountered

            Focus on understanding the customer's actual intent and needs, not just matching words.
            """,
            output_type=None
        )

    async def tag_conversation(self, messages: List[str], session_id: Optional[str] = None) -> TaggingResult:
        """
        Tag a conversation using AI agent analysis.

        Args:
            messages: List of user message texts
            session_id: Optional session ID for conversation continuity

        Returns:
            TaggingResult with AI-powered analysis
        """
        try:
            # Combine messages for analysis
            combined_text = " ".join(messages).strip()
            if not combined_text:
                return self._create_error_result("empty_input")

            # Check if OpenAI API is available
            if not OPENAI_AVAILABLE:
                logger.debug("OpenAI API not available. Using fallback analysis.")
                return self._fallback_analysis(combined_text)

            # Create or get session
            session = None
            if session_id:
                session = SQLiteSession(session_id, self.session_db_path)

            # Use the AI agent to analyze the conversation
            # The agent will use its natural language understanding based on the instructions
            result = await Runner.run(
                self.ai_agent,
                f"Analyze this customer conversation: {combined_text}",
                session=session
            )

            # Parse the AI response
            tagging_result = await self._parse_ai_response(result, combined_text)

            # Update metrics
            self._update_metrics(tagging_result.confidence_score)

            return tagging_result

        except Exception as e:
            logger.error(f"Error in agentic tagging: {str(e)}")
            self.metrics["error_count"] += 1
            return self._create_error_result("analysis_error")

    def _fallback_analysis(self, combined_text: str) -> TaggingResult:
        """Fallback analysis when OpenAI API is not available."""
        text_lower = combined_text.lower()

        # Simple fallback logic using basic keyword matching
        service_type = None
        category = None

        # Simple service detection
        if any(word in text_lower for word in ["flight", "plane", "airline", "booking reference"]):
            service_type = ServiceType.FLIGHT
        elif any(word in text_lower for word in ["hotel", "room", "reservation", "check-in"]):
            service_type = ServiceType.HOTEL
        elif any(word in text_lower for word in ["visa", "passport", "embassy"]):
            service_type = ServiceType.VISA
        elif any(word in text_lower for word in ["esim", "sim", "data", "roaming"]):
            service_type = ServiceType.ESIM
        elif any(word in text_lower for word in ["wallet", "balance", "payment", "money"]):
            service_type = ServiceType.WALLET

        # Simple category detection
        if any(word in text_lower for word in ["cancel", "refund", "terminate"]):
            category = Category.CANCELLATION
        elif any(word in text_lower for word in ["change", "modify", "update", "reschedule"]):
            category = Category.MODIFY
        elif any(word in text_lower for word in ["top up", "recharge", "add money"]):
            category = Category.TOP_UP
        elif any(word in text_lower for word in ["withdraw", "cash out", "take out"]):
            category = Category.WITHDRAW
        elif any(word in text_lower for word in ["check", "status", "verify", "confirm"]):
            category = Category.ORDER_RECHECK
        elif any(word in text_lower for word in ["how to", "can i", "information", "help"]):
            category = Category.PRE_PURCHASE

        # Determine confidence based on what was found
        if service_type and category:
            confidence = 0.7  # High confidence if both found
        elif service_type or category:
            confidence = 0.5  # Medium confidence if one found
        else:
            confidence = 0.3  # Low confidence if nothing found
            service_type = ServiceType.OTHER
            category = Category.OTHERS

        return TaggingResult(
            service_type=service_type,
            category=category,
            confidence_score=confidence,
            method_used="agentic_fallback",
            reasoning="Fallback analysis due to missing OpenAI API key - basic keyword matching used",
            key_phrases=self._extract_key_phrases(combined_text),
            metadata={
                "fallback_mode": True,
                "api_key_missing": True
            },
            timestamp=datetime.utcnow()
        )

    async def _parse_ai_response(self, agent_result, combined_text: str) -> TaggingResult:
        """Parse the AI agent response to extract tagging information."""
        try:
            # Extract information from AI response
            response_text = agent_result.final_output

            # Parse service type and category from AI response
            service_type, category, confidence, reasoning = self._extract_tagging_from_ai_response(response_text)

            # Extract key phrases from the original text
            key_phrases = self._extract_key_phrases(combined_text)

            return TaggingResult(
                service_type=service_type,
                category=category,
                confidence_score=confidence,
                method_used="ai_agent_analysis",
                reasoning=reasoning or "AI-powered conversation analysis",
                key_phrases=key_phrases,
                metadata={
                    "agent_name": "Conversation Analysis Agent",
                    "model": "gpt-4o-mini",
                    "analysis_method": "LLM-based content analysis",
                    "processing_time": getattr(agent_result, 'processing_time', 0),
                    "session_used": hasattr(agent_result, 'session') and agent_result.session is not None
                },
                timestamp=datetime.utcnow()
            )

        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return self._create_error_result("parsing_error")

    def _extract_tagging_from_ai_response(self, response_text: str) -> Tuple[Optional[ServiceType], Optional[Category], float, str]:
        """Extract service type, category, confidence, and reasoning from AI response."""
        text_lower = response_text.lower()

        # Initialize defaults
        service_type = ServiceType.OTHER
        category = Category.OTHERS
        confidence = 0.5
        reasoning = response_text

        # Simple service type mapping based on AI response
        service_mapping = {
            "flight": ServiceType.FLIGHT,
            "hotel": ServiceType.HOTEL,
            "visa": ServiceType.VISA,
            "esim": ServiceType.ESIM,
            "e-sim": ServiceType.ESIM,
            "wallet": ServiceType.WALLET,
            "other": ServiceType.OTHER
        }

        # Look for service type in AI response
        for keyword, service in service_mapping.items():
            if keyword in text_lower:
                service_type = service
                break

        # Simple category mapping
        category_mapping = {
            "cancellation": Category.CANCELLATION,
            "cancel": Category.CANCELLATION,
            "modify": Category.MODIFY,
            "change": Category.MODIFY,
            "top_up": Category.TOP_UP,
            "top up": Category.TOP_UP,
            "withdraw": Category.WITHDRAW,
            "cash out": Category.WITHDRAW,
            "order_recheck": Category.ORDER_RECHECK,
            "order re-check": Category.ORDER_RECHECK,
            "check": Category.ORDER_RECHECK,
            "status": Category.ORDER_RECHECK,
            "pre_purchase": Category.PRE_PURCHASE,
            "pre-purchase": Category.PRE_PURCHASE,
            "information": Category.PRE_PURCHASE,
            "help": Category.PRE_PURCHASE,
            "others": Category.OTHERS,
            "other": Category.OTHERS
        }

        # Look for category in AI response
        for keyword, cat in category_mapping.items():
            if keyword in text_lower:
                category = cat
                break

        # Extract confidence score from AI response
        import re
        confidence_match = re.search(r'confidence[:\s]*(\d*\.?\d+)', text_lower)
        if confidence_match:
            try:
                confidence = min(1.0, max(0.0, float(confidence_match.group(1))))
            except ValueError:
                confidence = 0.7

        return service_type, category, confidence, reasoning

    def _update_metrics(self, confidence: float):
        """Update performance metrics."""
        self.metrics["total_taggings"] += 1

        # Track successful taggings (confidence > 0.5)
        if confidence > 0.5:
            self.metrics["successful_taggings"] += 1

        # Update average confidence
        current_avg = self.metrics["average_confidence"]
        total = self.metrics["total_taggings"]
        self.metrics["average_confidence"] = (current_avg * (total - 1) + confidence) / total

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text."""
        # Simple extraction - in real implementation would use NLP
        words = text.lower().split()
        key_phrases = []

        # Look for common trigger phrases
        triggers = [
            'cancel', 'change', 'book', 'reserve', 'check', 'help',
            'flight', 'hotel', 'visa', 'esim', 'wallet', 'payment',
            'booking', 'reservation', 'refund', 'modify', 'top up',
            'withdraw', 'recharge', 'status', 'verify', 'confirm'
        ]

        for trigger in triggers:
            if trigger in words:
                key_phrases.append(trigger)

        return list(set(key_phrases))

    def _create_error_result(self, reason: str) -> TaggingResult:
        """Create an error result."""
        return TaggingResult(
            service_type=ServiceType.OTHER,
            category=Category.OTHERS,
            confidence_score=0.0,
            method_used="agentic_error",
            reasoning=f"Agentic analysis failed: {reason}",
            key_phrases=[],
            metadata={"error": reason},
            timestamp=datetime.utcnow()
        )

    def _update_metrics(self, agent_type: str, confidence: float):
        """Update performance metrics."""
        self.metrics["total_taggings"] += 1

        # Update agent usage
        agent_key = agent_type.replace("_agent", "").replace("general", "general_agent")
        if agent_key in self.metrics["agent_usage"]:
            self.metrics["agent_usage"][agent_key] += 1

        # Update average confidence
        current_avg = self.metrics["average_confidence"]
        total = self.metrics["total_taggings"]
        self.metrics["average_confidence"] = (current_avg * (total - 1) + confidence) / total

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        total_taggings = self.metrics["total_taggings"]
        successful_taggings = self.metrics["successful_taggings"]

        return {
            **self.metrics,
            "uptime_seconds": (datetime.utcnow() - self.metrics["last_reset"]).total_seconds(),
            "success_rate": successful_taggings / total_taggings if total_taggings > 0 else 0.0,
            "error_rate": self.metrics["error_count"] / total_taggings if total_taggings > 0 else 0.0
        }

    def reset_metrics(self):
        """Reset all performance metrics."""
        self.metrics = {
            "total_taggings": 0,
            "successful_taggings": 0,
            "average_confidence": 0.0,
            "error_count": 0,
            "last_reset": datetime.utcnow()
        }

    async def explain_tagging(self, messages: List[str]) -> Dict[str, Any]:
        """Explain the AI agent tagging process."""
        combined_text = " ".join(messages)

        # Perform actual tagging to show the process
        try:
            result = await self.tag_conversation(messages)
            actual_result = {
                "service_type": result.service_type.value if result.service_type else None,
                "category": result.category.value if result.category else None,
                "confidence_score": result.confidence_score,
                "method_used": result.method_used,
                "key_phrases": result.key_phrases
            }
        except Exception as e:
            actual_result = {"error": str(e)}

        return {
            'method': 'pure_llm_analysis',
            'agent_system': {
                'ai_agent': 'Single intelligent agent using pure LLM analysis',
                'capabilities': [
                    'Natural language understanding',
                    'Context-aware semantic analysis',
                    'Intent recognition beyond keywords',
                    'Pure AI-driven classification'
                ]
            },
            'conversation_analysis': {
                'length': len(messages),
                'combined_text_length': len(combined_text),
                'analysis_method': 'Pure LLM without keyword tools'
            },
            'actual_tagging_result': actual_result,
            'metrics': self.get_performance_metrics()
        }


# Example usage and testing
async def example_usage():
    """
    Example of how to use the pure LLM-based AI agent tagging system.
    """
    import asyncio
    import os

    # Set your OpenAI API key
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"

    # Initialize the engine
    engine = AgenticTaggingEngine()

    # Example conversations
    test_conversations = [
        # Flight booking
        ["I want to book a flight to Paris", "When are the cheapest flights?"],

        # Hotel reservation
        ["I need to cancel my hotel booking", "PNR is ABC123"],

        # Visa application
        ["I need to apply for a visa", "What documents do I need?"],

        # eSIM purchase
        ["How do I buy an eSIM for my trip?", "I need data roaming"],

        # Wallet operation
        ["How do I top up my wallet?", "I need to add money"],

        # Ambiguous request
        ["I need help with my booking"]
    ]

    for i, messages in enumerate(test_conversations):
        print(f"\n--- Test Conversation {i+1} ---")
        print(f"Messages: {messages}")

        try:
            # Tag the conversation using pure LLM
            result = await engine.tag_conversation(messages)
            print(f"Service Type: {result.service_type.value if result.service_type else 'None'}")
            print(f"Category: {result.category.value if result.category else 'None'}")
            print(".2f")
            print(f"Method: {result.method_used}")
            print(f"Reasoning: {result.reasoning[:100]}...")

        except Exception as e:
            print(f"Error: {e}")

    # Show performance metrics
    print("\n--- Performance Metrics ---")
    metrics = engine.get_performance_metrics()
    print(f"Total Taggings: {metrics['total_taggings']}")
    print(f"Successful Taggings: {metrics['successful_taggings']}")
    print(".2f")
    print(".1%")
    print(".1%")


if __name__ == "__main__":
    asyncio.run(example_usage())
