"""
Main application entry point with layered architecture.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os
from dotenv import load_dotenv

from .presentation.api.routes import router
from .presentation.web_ui.dashboard import create_dashboard_app

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create main FastAPI app
app = FastAPI(
    title="Sindibad Ticket Tagging Service - Layered Architecture",
    description="Intelligent automated ticket tagging and routing service with layered architecture",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["API"])

# Mount dashboard
dashboard_app = create_dashboard_app()
app.mount("/dashboard", dashboard_app, name="dashboard")

# Mount static files for dashboard
static_dir = os.path.join(os.path.dirname(__file__), "presentation", "web_ui")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Sindibad Ticket Tagging Service - Layered Architecture",
        "version": "3.0.0",
        "architecture": {
            "layers": ["presentation", "application", "domain", "infrastructure"],
            "tagging_layers": ["keywords", "agentic"]
        },
        "features": {
            "layered_architecture": True,
            "two_layer_tagging": True,
            "real_time_dashboard": True,
            "rest_api": True,
            "async_operations": True
        },
        "endpoints": {
            "api": "/api/docs",
            "dashboard": "/dashboard",
            "chat": "/dashboard/chat",
            "health": "/api/health",
            "tickets": "/api/tickets",
            "webhook": "/api/webhooks/messages"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Sindibad Ticket Tagging Service with layered architecture...")
    logger.info("Layers initialized: Domain, Application, Infrastructure, Presentation")
    logger.info("Tagging layers: Keywords (Layer 1), Agentic (Layer 2)")

    # Validate environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key and openai_api_key != "sk-your-openai-api-key-here":
        logger.info("OpenAI API key loaded successfully")
    else:
        logger.warning("OpenAI API key not set or using placeholder. AI features will use fallback mode.")

    # Log other important environment variables
    app_env = os.getenv("APP_ENV", "development")
    debug_mode = os.getenv("DEBUG", "False").lower() == "true"
    logger.info(f"Environment: {app_env}, Debug mode: {debug_mode}")

    # Initialize database
    from .infrastructure.database.ticket_repository import TicketRepository
    repo = TicketRepository()
    await repo.initialize_database()
    logger.info("Database initialized successfully")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
