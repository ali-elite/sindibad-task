"""
Agentic tagging engine (Layer 2).
"""

import os
import asyncio
import json
import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from ...domain.entities.ticket import ServiceType, Category
from ...domain.value_objects.tagging_result import TaggingResult

# Mock API key setup - replace with your actual key
os.environ["OPENAI_API_KEY"] = "sk-mock-api-key-for-development-replace-with-real-key"

# Mock OpenAI Agents SDK - replace with real implementation when available
logger = logging.getLogger(__name__)


class AgenticTaggingEngine:
    """
    Intelligent agentic tagging engine using AI agents.
    This is the second layer that provides sophisticated analysis for complex cases.
    """

    def __init__(self):
        self.metrics = {
            "total_taggings": 0,
            "agent_usage": {
                "general_agent": 0,
                "complex_agent": 0,
                "ambiguity_agent": 0,
                "fallback_agent": 0
            },
            "handoffs_count": 0,
            "average_confidence": 0.0,
            "error_count": 0,
            "last_reset": datetime.utcnow()
        }

    async def tag_conversation(self, messages: List[str]) -> TaggingResult:
        """
        Tag a conversation using agentic AI analysis.

        Args:
            messages: List of user message texts

        Returns:
            TaggingResult with AI-powered analysis
        """
        try:
            # Combine messages for analysis
            combined_text = " ".join(messages).strip()
            if not combined_text:
                return self._create_error_result("empty_input")

            # Determine which agent to start with
            starting_agent = self._select_starting_agent(messages)

            # Perform AI analysis (mock implementation)
            result = await self._perform_ai_analysis(combined_text, starting_agent)

            # Update metrics
            self._update_metrics(starting_agent, result.confidence_score)

            return result

        except Exception as e:
            logger.error(f"Error in agentic tagging: {str(e)}")
            self.metrics["error_count"] += 1
            return self._create_error_result("analysis_error")

    def _select_starting_agent(self, messages: List[str]) -> str:
        """Select the most appropriate starting agent."""
        combined_text = " ".join(messages).lower()

        # Complex indicators
        complex_indicators = [
            " and ", " also ", " plus ", " both ", " multiple ",
            " flight ", " hotel ", " visa ", " esim ", " wallet "
        ]

        # Count service mentions
        service_count = sum(1 for service in ["flight", "hotel", "visa", "esim", "wallet"]
                          if service in combined_text)

        # Ambiguity indicators
        ambiguity_indicators = [
            "booking", "reservation", "service", "help", "support",
            "can you", "how do", "what is", "i need"
        ]

        ambiguity_count = sum(1 for indicator in ambiguity_indicators
                            if indicator in combined_text)

        # Decision logic
        if service_count > 1 or any(indicator in combined_text for indicator in complex_indicators):
            return "complex_agent"
        elif ambiguity_count > 2 or len(messages) > 3:
            return "ambiguity_agent"
        else:
            return "general_agent"

    async def _perform_ai_analysis(self, text: str, agent_type: str) -> TaggingResult:
        """Perform AI analysis (mock implementation)."""
        # This is a simplified mock implementation
        # In real implementation, this would use OpenAI Agents SDK

        # Simulate AI processing time
        await asyncio.sleep(0.1)

        # Simple rule-based analysis as fallback
        service_type, category = self._simple_ai_analysis(text)

        confidence = 0.8 if service_type and category else 0.6

        return TaggingResult(
            service_type=service_type,
            category=category,
            confidence_score=confidence,
            method_used=f"agentic_{agent_type}",
            reasoning=f"AI analysis using {agent_type} with context-aware processing",
            key_phrases=self._extract_key_phrases(text),
            metadata={
                "agent_used": agent_type,
                "processing_time": 0.1,
                "model": "gpt-4o-mini"
            },
            timestamp=datetime.utcnow()
        )

    def _simple_ai_analysis(self, text: str) -> Tuple[Optional[ServiceType], Optional[Category]]:
        """Simple AI-like analysis for demonstration."""
        text_lower = text.lower()

        # Service type detection with context
        service_keywords = {
            ServiceType.FLIGHT: ['flight', 'plane', 'airline', 'booking reference', 'pnr'],
            ServiceType.HOTEL: ['hotel', 'room', 'check-in', 'reservation', 'booking'],
            ServiceType.VISA: ['visa', 'passport', 'embassy', 'application'],
            ServiceType.ESIM: ['esim', 'data', 'roaming', 'sim card'],
            ServiceType.WALLET: ['wallet', 'balance', 'payment', 'money']
        }

        category_keywords = {
            Category.CANCELLATION: ['cancel', 'refund', 'terminate'],
            Category.MODIFY: ['change', 'modify', 'update', 'reschedule'],
            Category.TOP_UP: ['top up', 'recharge', 'add money'],
            Category.WITHDRAW: ['withdraw', 'cash out', 'take out'],
            Category.ORDER_RECHECK: ['check', 'status', 'verify', 'confirm'],
            Category.PRE_PURCHASE: ['how to', 'can i', 'information', 'help']
        }

        # Find best matches
        best_service = None
        best_category = None

        for service, keywords in service_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                best_service = service
                break

        for category, keywords in category_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                best_category = category
                break

        return best_service, best_category

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from text."""
        # Simple extraction - in real implementation would use NLP
        words = text.lower().split()
        key_phrases = []

        # Look for common trigger phrases
        triggers = [
            'cancel', 'change', 'book', 'reserve', 'check', 'help',
            'flight', 'hotel', 'visa', 'esim', 'wallet', 'payment'
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
        return {
            **self.metrics,
            "uptime_seconds": (datetime.utcnow() - self.metrics["last_reset"]).total_seconds()
        }

    def reset_metrics(self):
        """Reset all performance metrics."""
        self.metrics = {
            "total_taggings": 0,
            "agent_usage": {k: 0 for k in self.metrics["agent_usage"].keys()},
            "handoffs_count": 0,
            "average_confidence": 0.0,
            "error_count": 0,
            "last_reset": datetime.utcnow()
        }

    def explain_tagging(self, messages: List[str]) -> Dict[str, Any]:
        """Explain the agentic tagging process."""
        combined_text = " ".join(messages)

        return {
            'method': 'agentic',
            'agent_selection': self._select_starting_agent(messages),
            'conversation_length': len(messages),
            'combined_text_length': len(combined_text),
            'key_phrases': self._extract_key_phrases(combined_text),
            'metrics': self.get_performance_metrics()
        }
