"""
API routes for the ticket tagging service.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime

from ...application.use_cases.process_message import ProcessMessageUseCase
from ...application.use_cases.get_ticket_details import GetTicketDetailsUseCase
from ...application.use_cases.list_tickets import ListTicketsUseCase
from ...application.use_cases.update_ticket_status import UpdateTicketStatusUseCase
from ...application.use_cases.get_tagging_explanation import GetTaggingExplanationUseCase
from ...domain.entities.ticket import TicketStatus
from .dependencies import get_ticket_service, get_tagging_service

# Create router
router = APIRouter()

# Initialize use cases
_process_message_use_case = None
_get_ticket_details_use_case = None
_list_tickets_use_case = None
_update_ticket_status_use_case = None
_get_tagging_explanation_use_case = None


def get_process_message_use_case():
    global _process_message_use_case
    if _process_message_use_case is None:
        _process_message_use_case = ProcessMessageUseCase(get_ticket_service())
    return _process_message_use_case


def get_ticket_details_use_case():
    global _get_ticket_details_use_case
    if _get_ticket_details_use_case is None:
        _get_ticket_details_use_case = GetTicketDetailsUseCase(get_ticket_service())
    return _get_ticket_details_use_case


def get_list_tickets_use_case():
    global _list_tickets_use_case
    if _list_tickets_use_case is None:
        _list_tickets_use_case = ListTicketsUseCase(get_ticket_service())
    return _list_tickets_use_case


def get_update_ticket_status_use_case():
    global _update_ticket_status_use_case
    if _update_ticket_status_use_case is None:
        _update_ticket_status_use_case = UpdateTicketStatusUseCase(get_ticket_service())
    return _update_ticket_status_use_case


def get_tagging_explanation_use_case():
    global _get_tagging_explanation_use_case
    if _get_tagging_explanation_use_case is None:
        _get_tagging_explanation_use_case = GetTaggingExplanationUseCase(
            get_ticket_service(), get_tagging_service()
        )
    return _get_tagging_explanation_use_case


@router.post("/webhooks/messages")
async def receive_message_webhook(
    payload: Dict[str, Any],
    use_case = Depends(get_process_message_use_case)
):
    """
    Webhook endpoint to receive messages from chat service.
    Creates new tickets or appends messages to existing ones.
    """
    try:
        conversation_id = payload.get("conversation_id")
        messages = payload.get("messages", [])

        if not conversation_id or not messages:
            raise HTTPException(status_code=400, detail="Missing conversation_id or messages")

        result = await use_case.execute(conversation_id, messages)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/tickets")
async def get_all_tickets(
    limit: int = 50,
    offset: int = 0,
    use_case = Depends(get_list_tickets_use_case)
):
    """Get all tickets with pagination."""
    try:
        result = await use_case.execute(limit=limit, offset=offset)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    use_case = Depends(get_ticket_details_use_case)
):
    """Get a specific ticket by ID."""
    try:
        result = await use_case.execute(ticket_id)

        if not result:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/tickets/{ticket_id}/status")
async def update_ticket_status(
    ticket_id: str,
    status: TicketStatus,
    use_case = Depends(get_update_ticket_status_use_case)
):
    """Update ticket status."""
    try:
        result = await use_case.execute(ticket_id, status)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/tickets/{ticket_id}/tags/explain")
async def explain_ticket_tags(
    ticket_id: str,
    use_case = Depends(get_tagging_explanation_use_case)
):
    """Get explanation for why certain tags were applied to a ticket."""
    try:
        result = await use_case.execute(ticket_id)

        if not result:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0.0",
        "architecture": "layered"
    }


@router.get("/stats")
async def get_ticket_stats(ticket_service = Depends(get_ticket_service)):
    """Get ticket statistics."""
    try:
        stats = await ticket_service.get_ticket_stats()
        return {
            "status": "success",
            "stats": stats,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
