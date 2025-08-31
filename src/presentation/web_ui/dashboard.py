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

    @dashboard_app.get("/api/tickets/realtime")
    async def get_realtime_tickets():
        """Endpoint for real-time ticket updates."""
        # This would be replaced with actual database queries
        return {
            "tickets": [],
            "stats": {
                "total": 0,
                "open": 0,
                "closed": 0
            }
        }

    return dashboard_app
