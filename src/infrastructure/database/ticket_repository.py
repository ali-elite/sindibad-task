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
        """Get comprehensive ticket statistics."""
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

            # Category distribution
            category_stmt = select(
                TicketModel.category,
                func.count(TicketModel.ticket_id).label('count')
            ).where(TicketModel.category.isnot(None)).group_by(TicketModel.category)

            category_result = await session.execute(category_stmt)
            category_distribution = {row.category: row.count for row in category_result}

            # Tagging method distribution
            method_stmt = select(
                TicketModel.method,
                func.count(TicketModel.ticket_id).label('count')
            ).where(TicketModel.method.isnot(None)).group_by(TicketModel.method)

            method_result = await session.execute(method_stmt)
            method_distribution = {row.method: row.count for row in method_result}

            # Confidence statistics
            confidence_stmt = select(
                func.avg(TicketModel.confidence).label('avg_confidence'),
                func.min(TicketModel.confidence).label('min_confidence'),
                func.max(TicketModel.confidence).label('max_confidence'),
                func.count(case((TicketModel.confidence >= 0.8, 1))).label('high_confidence_count'),
                func.count(case((TicketModel.confidence < 0.5, 1))).label('low_confidence_count')
            )
            confidence_result = await session.execute(confidence_stmt)
            confidence_stats = confidence_result.first()

            # Automation metrics
            automated_stmt = select(
                func.count(case((TicketModel.method != 'manual', 1))).label('automated_count'),
                func.count(case((TicketModel.method == 'manual', 1))).label('manual_count')
            )
            automated_result = await session.execute(automated_stmt)
            automated_stats = automated_result.first()

            # Time-based metrics (last 24 hours)
            from datetime import datetime, timedelta
            yesterday = datetime.utcnow() - timedelta(days=1)

            recent_stmt = select(func.count(TicketModel.ticket_id)).where(TicketModel.created_at >= yesterday)
            recent_result = await session.execute(recent_stmt)
            recent_tickets = recent_result.scalar()

            # Calculate derived KPIs
            total_with_tags = sum(service_distribution.values())
            automation_rate = (automated_stats.automated_count / total_tickets * 100) if total_tickets > 0 else 0
            avg_confidence = confidence_stats.avg_confidence * 100 if confidence_stats.avg_confidence else 0
            high_confidence_rate = (confidence_stats.high_confidence_count / total_with_tags * 100) if total_with_tags > 0 else 0
            low_confidence_rate = (confidence_stats.low_confidence_count / total_with_tags * 100) if total_with_tags > 0 else 0

            return {
                "total_tickets": total_tickets,
                "recent_tickets_24h": recent_tickets,
                "status_distribution": status_distribution,
                "service_distribution": service_distribution,
                "category_distribution": category_distribution,
                "method_distribution": method_distribution,
                "confidence_stats": {
                    "average": f"{avg_confidence:.1f}%",
                    "high_confidence_rate": f"{high_confidence_rate:.1f}%",
                    "low_confidence_rate": f"{low_confidence_rate:.1f}%",
                    "min": f"{(confidence_stats.min_confidence or 0) * 100:.1f}%",
                    "max": f"{(confidence_stats.max_confidence or 0) * 100:.1f}%"
                },
                "automation_metrics": {
                    "automation_rate": f"{automation_rate:.1f}%",
                    "automated_count": automated_stats.automated_count,
                    "manual_count": automated_stats.manual_count
                },
                "tagging_quality": {
                    "tagged_tickets": total_with_tags,
                    "untagged_rate": f"{((total_tickets - total_with_tags) / total_tickets * 100):.1f}%" if total_tickets > 0 else "0%"
                }
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

    async def get_corner_case_stats(self) -> Dict[str, Any]:
        """Get comprehensive corner case statistics."""
        async with self.session_factory() as session:
            # Total tickets for reference
            total_stmt = select(func.count(TicketModel.ticket_id))
            total_result = await session.execute(total_stmt)
            total_tickets = total_result.scalar() or 0

            # Low confidence tickets (< 50%)
            low_confidence_stmt = select(func.count(TicketModel.ticket_id)).where(TicketModel.confidence < 0.5)
            low_confidence_result = await session.execute(low_confidence_stmt)
            low_confidence_count = low_confidence_result.scalar() or 0

            # Default fallback tickets (Other/Others)
            default_fallback_stmt = select(func.count(TicketModel.ticket_id)).where(
                (TicketModel.service_type == "Other") & (TicketModel.category == "Others")
            )
            default_fallback_result = await session.execute(default_fallback_stmt)
            default_fallback_count = default_fallback_result.scalar() or 0

            # Missing classifications
            missing_service_stmt = select(func.count(TicketModel.ticket_id)).where(TicketModel.service_type.is_(None))
            missing_service_result = await session.execute(missing_service_stmt)
            missing_service_count = missing_service_result.scalar() or 0

            missing_category_stmt = select(func.count(TicketModel.ticket_id)).where(TicketModel.category.is_(None))
            missing_category_result = await session.execute(missing_category_stmt)
            missing_category_count = missing_category_result.scalar() or 0

            # Method distribution for corner cases
            method_stmt = select(
                TicketModel.method,
                func.count(TicketModel.ticket_id).label('count')
            ).where(TicketModel.confidence < 0.5).group_by(TicketModel.method)
            method_result = await session.execute(method_stmt)
            method_distribution = {row.method: row.count for row in method_result}

            # Confidence distribution for corner cases
            confidence_ranges_stmt = select(
                func.count(case((TicketModel.confidence < 0.3, 1))).label('very_low'),
                func.count(case((TicketModel.confidence.between(0.3, 0.5), 1))).label('low'),
                func.count(case((TicketModel.confidence.between(0.5, 0.7), 1))).label('medium'),
                func.count(case((TicketModel.confidence >= 0.7, 1))).label('high')
            )
            confidence_ranges_result = await session.execute(confidence_ranges_stmt)
            confidence_ranges = confidence_ranges_result.first()

            # Calculate percentages
            low_confidence_rate = (low_confidence_count / total_tickets * 100) if total_tickets > 0 else 0
            default_fallback_rate = (default_fallback_count / total_tickets * 100) if total_tickets > 0 else 0
            missing_classification_rate = ((missing_service_count + missing_category_count) / total_tickets * 100) if total_tickets > 0 else 0

            return {
                "total_corner_cases": low_confidence_count + default_fallback_count + missing_service_count + missing_category_count,
                "corner_case_rate": f"{((low_confidence_count + default_fallback_count + missing_service_count + missing_category_count) / total_tickets * 100):.1f}%" if total_tickets > 0 else "0%",
                "breakdown": {
                    "low_confidence": {
                        "count": low_confidence_count,
                        "rate": f"{low_confidence_rate:.1f}%"
                    },
                    "default_fallback": {
                        "count": default_fallback_count,
                        "rate": f"{default_fallback_rate:.1f}%"
                    },
                    "missing_classifications": {
                        "count": missing_service_count + missing_category_count,
                        "rate": f"{missing_classification_rate:.1f}%",
                        "service_missing": missing_service_count,
                        "category_missing": missing_category_count
                    }
                },
                "confidence_distribution": {
                    "very_low_0_30": confidence_ranges.very_low if confidence_ranges else 0,
                    "low_30_50": confidence_ranges.low if confidence_ranges else 0,
                    "medium_50_70": confidence_ranges.medium if confidence_ranges else 0,
                    "high_70_100": confidence_ranges.high if confidence_ranges else 0
                },
                "method_distribution_corner_cases": method_distribution,
                "severity_levels": {
                    "critical": low_confidence_count + missing_service_count + missing_category_count,
                    "warning": default_fallback_count,
                    "info": confidence_ranges.medium if confidence_ranges else 0
                }
            }

    async def get_problematic_tickets(self, limit: int = 20) -> List[Ticket]:
        """Get tickets that represent corner cases ordered by severity."""
        async with self.session_factory() as session:
            # Build query for problematic tickets
            stmt = select(TicketModel).options(selectinload(TicketModel.messages))

            # Order by severity: low confidence first, then missing classifications, then default fallbacks
            stmt = stmt.order_by(
                TicketModel.confidence.asc(),  # Lowest confidence first
                case(
                    (TicketModel.service_type.is_(None), 1),
                    (TicketModel.category.is_(None), 1),
                    ((TicketModel.service_type == "Other") & (TicketModel.category == "Others"), 1),
                    else_=0
                ).desc(),
                TicketModel.created_at.desc()
            ).limit(limit)

            result = await session.execute(stmt)
            ticket_models = result.scalars().all()

            return [ticket_model.to_domain_entity() for ticket_model in ticket_models]
