"""
Real-time dashboard for ticket monitoring.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os


def create_dashboard_app() -> FastAPI:
    """Create the dashboard FastAPI application."""

    dashboard_app = FastAPI(title="Sindibad Ticket Dashboard")

    # Get the directory of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Mount static files
    dashboard_app.mount("/static", StaticFiles(directory=current_dir), name="static")

    # Setup templates
    templates = Jinja2Templates(directory=current_dir)

    @dashboard_app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Main dashboard page."""
        return templates.TemplateResponse("index.html", {"request": request})

    @dashboard_app.get("/chat", response_class=HTMLResponse)
    async def chat_interface(request: Request):
        """Chat service mock interface."""
        return templates.TemplateResponse("chat.html", {"request": request})

    @dashboard_app.get("/api/tickets/realtime")
    async def get_realtime_tickets():
        """Endpoint for real-time ticket updates."""
        # Import services here to avoid circular imports
        from ...application.services.ticket_service import TicketService

        try:
            ticket_service = TicketService()
            tickets = await ticket_service.get_all_tickets(limit=20)
            stats = await ticket_service.get_ticket_stats()
            corner_case_stats = await ticket_service.get_corner_case_stats()

            # Format tickets for the dashboard
            formatted_tickets = []
            total_confidence = 0
            ticket_count = 0

            for ticket in tickets:
                if ticket.current_tag.confidence > 0:
                    total_confidence += ticket.current_tag.confidence
                    ticket_count += 1

                formatted_tickets.append({
                    "ticket_id": ticket.ticket_id[:8] + "...",  # Shorten for display
                    "conversation_id": ticket.conversation_id,
                    "service_type": ticket.current_tag.service_type.value if ticket.current_tag.service_type else "Other",
                    "category": ticket.current_tag.category.value if ticket.current_tag.category else "Others",
                    "confidence": f"{ticket.current_tag.confidence:.2%}",
                    "method": ticket.current_tag.method,
                    "status": ticket.status.value,
                    "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M"),
                    # Add corner case flags
                    "is_corner_case": _is_corner_case_ticket(ticket),
                    "corner_case_type": _get_corner_case_type(ticket)
                })

            return {
                "tickets": formatted_tickets,
                "stats": stats,
                "corner_cases": corner_case_stats
            }
        except Exception as e:
            print(f"Dashboard error: {e}")
            return {
                "tickets": [],
                "stats": {
                    "total_tickets": 0,
                    "recent_tickets_24h": 0,
                    "status_distribution": {},
                    "service_distribution": {},
                    "category_distribution": {},
                    "method_distribution": {},
                    "confidence_stats": {
                        "average": "0%",
                        "high_confidence_rate": "0%",
                        "low_confidence_rate": "0%"
                    },
                    "automation_metrics": {
                        "automation_rate": "0%",
                        "automated_count": 0,
                        "manual_count": 0
                    },
                    "tagging_quality": {
                        "tagged_tickets": 0,
                        "untagged_rate": "0%"
                    }
                }
            }

    @dashboard_app.get("/api/kpis/summary")
    async def get_kpi_summary():
        """Get KPI summary for dashboard overview."""
        from ...application.services.ticket_service import TicketService

        try:
            ticket_service = TicketService()
            stats = await ticket_service.get_ticket_stats()

            return {
                "north_star": {
                    "metric": "Automation Rate",
                    "value": stats["automation_metrics"]["automation_rate"],
                    "target": "85%",
                    "trend": "up"  # This would be calculated based on historical data
                },
                "secondary_kpis": [
                    {
                        "name": "High Confidence Rate",
                        "value": stats["confidence_stats"]["high_confidence_rate"],
                        "target": "75%"
                    },
                    {
                        "name": "Avg Tagging Accuracy",
                        "value": stats["confidence_stats"]["average"],
                        "target": "80%"
                    },
                    {
                        "name": "Untagged Rate",
                        "value": stats["tagging_quality"]["untagged_rate"],
                        "target": "<5%"
                    }
                ],
                "efficiency_metrics": [
                    {
                        "name": "Total Tickets",
                        "value": stats["total_tickets"],
                        "change": f"+{stats['recent_tickets_24h']} in 24h"
                    },
                    {
                        "name": "Automated Tickets",
                        "value": stats["automation_metrics"]["automated_count"],
                        "percentage": stats["automation_metrics"]["automation_rate"]
                    }
                ]
            }
        except Exception as e:
            print(f"KPI summary error: {e}")
            return {"error": str(e)}

    @dashboard_app.get("/api/analytics/trends")
    async def get_analytics_trends():
        """Get analytics trends data."""
        # This would typically fetch from a time-series database
        # For now, return mock trend data
        return {
            "automation_trend": [
                {"date": "2024-01-01", "value": 45.2},
                {"date": "2024-01-02", "value": 52.1},
                {"date": "2024-01-03", "value": 58.3},
                {"date": "2024-01-04", "value": 61.7},
                {"date": "2024-01-05", "value": 65.2},
                {"date": "2024-01-06", "value": 68.9},
                {"date": "2024-01-07", "value": 72.1}
            ],
            "accuracy_trend": [
                {"date": "2024-01-01", "value": 72.3},
                {"date": "2024-01-02", "value": 74.1},
                {"date": "2024-01-03", "value": 76.8},
                {"date": "2024-01-04", "value": 78.2},
                {"date": "2024-01-05", "value": 79.7},
                {"date": "2024-01-06", "value": 81.3},
                {"date": "2024-01-07", "value": 82.9}
            ]
                    }

    @dashboard_app.get("/api/corner-cases/detailed")
    async def get_corner_case_details():
        """Get detailed corner case analysis."""
        from ...application.services.ticket_service import TicketService

        try:
            ticket_service = TicketService()
            corner_case_stats = await ticket_service.get_corner_case_stats()
            problematic_tickets = await ticket_service.get_problematic_tickets(limit=10)

            return {
                "corner_case_stats": corner_case_stats,
                "problematic_tickets": [
                    {
                        "ticket_id": ticket.ticket_id[:8] + "...",
                        "conversation_id": ticket.conversation_id,
                        "service_type": ticket.current_tag.service_type.value if ticket.current_tag.service_type else "Other",
                        "category": ticket.current_tag.category.value if ticket.current_tag.category else "Others",
                        "confidence": f"{ticket.current_tag.confidence:.2%}",
                        "method": ticket.current_tag.method,
                        "issues": _get_ticket_issues(ticket),
                        "message_preview": ticket.get_combined_text()[:100] + "..." if len(ticket.get_combined_text()) > 100 else ticket.get_combined_text(),
                        "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M")
                    }
                    for ticket in problematic_tickets
                ]
            }
        except Exception as e:
            print(f"Corner case details error: {e}")
            return {"error": str(e)}

    return dashboard_app


def _is_corner_case_ticket(ticket) -> bool:
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


def _get_corner_case_type(ticket) -> str:
    """Get the type of corner case for a ticket."""
    if ticket.current_tag.confidence < 0.5:
        return "low_confidence"
    elif ticket.current_tag.is_default_tag:
        return "default_fallback"
    elif not ticket.current_tag.service_type or not ticket.current_tag.category:
        return "missing_classification"
    elif len(ticket.get_user_messages()) == 0:
        return "no_user_messages"
    elif len(ticket.get_user_messages()) > 10:
        return "long_conversation"
    elif len(ticket.get_combined_text().strip()) < 10:
        return "short_message"
    else:
        return "other"


def _get_ticket_issues(ticket) -> list:
    """Get list of issues for a ticket."""
    issues = []

    if ticket.current_tag.confidence < 0.5:
        issues.append("Low confidence")
    if ticket.current_tag.is_default_tag:
        issues.append("Default fallback")
    if not ticket.current_tag.service_type:
        issues.append("Missing service type")
    if not ticket.current_tag.category:
        issues.append("Missing category")
    if len(ticket.get_user_messages()) == 0:
        issues.append("No user messages")
    if len(ticket.get_user_messages()) > 10:
        issues.append("Very long conversation")
    if len(ticket.get_combined_text().strip()) < 10:
        issues.append("Very short message")

    return issues
