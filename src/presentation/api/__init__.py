"""
Presentation API layer.
"""

from .routes import router
from .dependencies import get_ticket_service, get_tagging_service

__all__ = [
    "router",
    "get_ticket_service",
    "get_tagging_service",
]
