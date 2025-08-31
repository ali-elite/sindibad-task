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
                    "status": ticket.status.value,
                    "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M")
                })

            avg_confidence = (total_confidence / ticket_count * 100) if ticket_count > 0 else 0

            return {
                "tickets": formatted_tickets,
                "stats": {
                    "total": stats["total_tickets"],
                    "open": stats["status_distribution"].get("open", 0),
                    "closed": stats["status_distribution"].get("closed", 0),
                    "avg_confidence": f"{avg_confidence:.1f}%"
                },
                "service_distribution": stats["service_distribution"]
            }
        except Exception as e:
            print(f"Dashboard error: {e}")
            return {
                "tickets": [],
                "stats": {
                    "total": 0,
                    "open": 0,
                    "closed": 0,
                    "avg_confidence": "0%"
                },
                "service_distribution": {}
            }

    return dashboard_app
