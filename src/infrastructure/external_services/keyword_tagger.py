"""
Keyword-based tagging engine (Layer 1).
"""

import re
from typing import Optional, Tuple, Dict, List, Any
from ...domain.entities.ticket import ServiceType, Category
from ...domain.value_objects.tagging_result import TaggingResult
from datetime import datetime


class KeywordTaggingEngine:
    """
    Fast, rule-based tagging engine using keyword matching.
    This is the first layer that provides quick tagging with default fallbacks.
    """

    def __init__(self):
        # Service type keywords - order matters (more specific first)
        self.service_keywords = {
            ServiceType.FLIGHT: [
                'flight', 'flights', 'airline', 'airway', 'airplane', 'aircraft',
                'booking reference', 'pnr', 'departure', 'arrival', 'gate',
                'boarding', 'seat', 'baggage', 'check-in', 'terminal',
                'pilot', 'crew', 'turbulence', 'layover', 'connecting flight'
            ],
            ServiceType.HOTEL: [
                'hotel', 'hotels', 'accommodation', 'room', 'rooms', 'suite',
                'reservation', 'check-in', 'check-out', 'lobby', 'reception',
                'housekeeping', 'amenities', 'breakfast', 'pool', 'spa',
                'concierge', 'bed', 'bathroom', 'wifi', 'parking'
            ],
            ServiceType.VISA: [
                'visa', 'visas', 'passport', 'immigration', 'embassy', 'consulate',
                'application', 'documents', 'processing', 'approval', 'rejection',
                'tourist visa', 'business visa', 'transit visa', 'entry permit',
                'border', 'customs', 'documentation'
            ],
            ServiceType.ESIM: [
                'esim', 'e-sim', 'sim', 'data', 'roaming', 'network', 'cellular',
                'mobile data', 'internet', 'connectivity', 'signal', 'carrier',
                'data plan', 'gb', 'mb', 'unlimited data', 'coverage'
            ],
            ServiceType.WALLET: [
                'wallet', 'balance', 'payment', 'money', 'funds', 'account',
                'credit', 'debit', 'transaction', 'transfer', 'deposit',
                'withdrawal', 'refund', 'charge', 'billing', 'invoice'
            ]
        }

        # Category keywords - order matters (more specific first)
        self.category_keywords = {
            Category.CANCELLATION: [
                'cancel', 'cancelled', 'cancellation', 'refund', 'abort',
                'terminate', 'stop', 'end', 'quit', 'remove', 'delete',
                'void', 'annul', 'revoke', 'withdraw booking'
            ],
            Category.MODIFY: [
                'change', 'modify', 'modification', 'update', 'edit', 'alter',
                'adjust', 'reschedule', 'postpone', 'move', 'shift',
                'different', 'another', 'switch', 'transfer', 'exchange'
            ],
            Category.TOP_UP: [
                'top up', 'topup', 'top-up', 'recharge', 'reload', 'add money',
                'add funds', 'deposit', 'credit', 'load', 'refill',
                'increase balance', 'add credit'
            ],
            Category.WITHDRAW: [
                'withdraw', 'withdrawal', 'cash out', 'take out', 'remove funds',
                'extract', 'get money', 'retrieve funds', 'debit',
                'transfer out', 'move money out'
            ],
            Category.ORDER_RECHECK: [
                'recheck', 're-check', 'review', 'verify', 'confirm', 'validate',
                'double check', 'examine', 'inspect', 'audit', 'status',
                'check order', 'order status', 'booking status'
            ],
            Category.PRE_PURCHASE: [
                'pre-purchase', 'pre purchase', 'before buying', 'inquiry',
                'question', 'ask', 'information', 'details', 'help',
                'support', 'how to', 'can i', 'is it possible', 'availability'
            ]
        }

        # Compile regex patterns for efficiency
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for keyword matching"""
        self.service_patterns = {}
        self.category_patterns = {}

        for service_type, keywords in self.service_keywords.items():
            # Create case-insensitive word boundary patterns
            patterns = [rf'\b{re.escape(keyword)}\b' for keyword in keywords]
            self.service_patterns[service_type] = re.compile('|'.join(patterns), re.IGNORECASE)

        for category, keywords in self.category_keywords.items():
            patterns = [rf'\b{re.escape(keyword)}\b' for keyword in keywords]
            self.category_patterns[category] = re.compile('|'.join(patterns), re.IGNORECASE)

    def tag_text(self, text: str) -> TaggingResult:
        """
        Tag text using keyword matching.

        Args:
            text: Input text to analyze

        Returns:
            TaggingResult with service type, category, and confidence
        """
        text_lower = text.lower().strip()

        # Find service type
        service_type, service_confidence = self._find_service_type(text_lower)

        # Find category
        category, category_confidence = self._find_category(text_lower)

        # If no matches found, return default "others-others"
        if not service_type and not category:
            return TaggingResult(
                service_type=ServiceType.OTHER,
                category=Category.OTHERS,
                confidence_score=0.0,
                method_used="keywords_default",
                reasoning="No keyword matches found, assigned default tags",
                key_phrases=[],
                metadata={"no_matches": True},
                timestamp=datetime.utcnow()
            )

        # Calculate overall confidence
        overall_confidence = max(service_confidence, category_confidence)

        return TaggingResult(
            service_type=service_type,
            category=category,
            confidence_score=overall_confidence,
            method_used="keywords",
            reasoning=self._generate_reasoning(text_lower, service_type, category),
            key_phrases=self._extract_key_phrases(text_lower),
            metadata={
                "service_confidence": service_confidence,
                "category_confidence": category_confidence
            },
            timestamp=datetime.utcnow()
        )

    def _find_service_type(self, text: str) -> Tuple[Optional[ServiceType], float]:
        """Find the most likely service type from text"""
        scores = {}

        for service_type, pattern in self.service_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Score based on number of matches and keyword specificity
                score = len(matches)
                # Boost score for more specific keywords (those appearing later in list)
                for match in matches:
                    keyword_index = next((i for i, kw in enumerate(self.service_keywords[service_type])
                                        if kw.lower() in match.lower()), 0)
                    score += keyword_index * 0.1  # Small boost for more specific terms

                scores[service_type] = score

        if scores:
            best_service = max(scores.items(), key=lambda x: x[1])
            # Normalize confidence score (0-1)
            confidence = min(best_service[1] * 0.3, 1.0)
            return best_service[0], confidence

        return None, 0.0

    def _find_category(self, text: str) -> Tuple[Optional[Category], float]:
        """Find the most likely category from text"""
        scores = {}

        for category, pattern in self.category_patterns.items():
            matches = pattern.findall(text)
            if matches:
                # Score based on number of matches and keyword specificity
                score = len(matches)
                # Boost score for more specific keywords
                for match in matches:
                    keyword_index = next((i for i, kw in enumerate(self.category_keywords[category])
                                        if kw.lower() in match.lower()), 0)
                    score += keyword_index * 0.1

                scores[category] = score

        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            # Normalize confidence score (0-1)
            confidence = min(best_category[1] * 0.3, 1.0)
            return best_category[0], confidence

        return None, 0.0

    def _generate_reasoning(self, text: str, service_type: Optional[ServiceType],
                           category: Optional[Category]) -> str:
        """Generate reasoning for the tagging decision."""
        reasons = []

        if service_type:
            pattern = self.service_patterns[service_type]
            matches = pattern.findall(text)
            if matches:
                reasons.append(f"Service type '{service_type.value}' matched keywords: {', '.join(matches)}")

        if category:
            pattern = self.category_patterns[category]
            matches = pattern.findall(text)
            if matches:
                reasons.append(f"Category '{category.value}' matched keywords: {', '.join(matches)}")

        return "; ".join(reasons) if reasons else "Keyword-based tagging"

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases that triggered the tagging."""
        key_phrases = []

        # Check all patterns for matches
        for service_type, pattern in self.service_patterns.items():
            matches = pattern.findall(text)
            key_phrases.extend(matches)

        for category, pattern in self.category_patterns.items():
            matches = pattern.findall(text)
            key_phrases.extend(matches)

        return list(set(key_phrases))  # Remove duplicates

    def explain_tagging(self, text: str) -> Dict[str, Any]:
        """Explain why certain tags were applied."""
        text_lower = text.lower().strip()
        explanation = {
            'method': 'keywords',
            'service_matches': [],
            'category_matches': [],
            'confidence_analysis': {}
        }

        # Find service matches
        for service_type, pattern in self.service_patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                explanation['service_matches'].extend([
                    f"{service_type.value}: {', '.join(matches)}"
                ])

        # Find category matches
        for category, pattern in self.category_patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                explanation['category_matches'].extend([
                    f"{category.value}: {', '.join(matches)}"
                ])

        return explanation
