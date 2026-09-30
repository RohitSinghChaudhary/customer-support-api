from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import db
from app.models import (
    IDResponse,
    MessageResponse,
    Ticket,
    TicketListResponse,
    TicketResponse
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])

def get_object_id(ticket_id: str):
    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket ID"
        )
    return ObjectId(ticket_id)

def get_customer_object_id(customer_id: str):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid customer ID"
        )
    return ObjectId(customer_id)

def serialize_ticket(ticket):
    return {
        "id": str(ticket["_id"]),
        "customer_id": str(ticket["customer_id"]),
        "subject": ticket["subject"],
        "description": ticket["description"],
        "status": ticket["status"]
    }

@router.post(
    "",
    response_model=IDResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(ticket: Ticket):
    customer_object_id = get_customer_object_id(
        ticket.customer_id
    )

    customer = db.customers.find_one(
        {"_id": customer_object_id}
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    ticket_data = ticket.model_dump()
    ticket_data["customer_id"] = customer_object_id

    result = db.tickets.insert_one(ticket_data)

    return {
        "message": "Ticket created",
        "id": str(result.inserted_id)
    }

@router.get(
    "",
    response_model=TicketListResponse
)
def get_tickets():
    tickets = [
        serialize_ticket(ticket)
        for ticket in db.tickets.find()
    ]

    return {"tickets": tickets}

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(ticket_id: str):
    object_id = get_object_id(ticket_id)

    ticket = db.tickets.find_one({"_id": object_id})

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return serialize_ticket(ticket)

@router.put(
    "/{ticket_id}",
    response_model=MessageResponse
)
def update_ticket(ticket_id: str, ticket: Ticket):
    ticket_object_id = get_object_id(ticket_id)
    customer_object_id = get_customer_object_id(
        ticket.customer_id
    )

    customer = db.customers.find_one(
        {"_id": customer_object_id}
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    ticket_data = ticket.model_dump()
    ticket_data["customer_id"] = customer_object_id

    result = db.tickets.update_one(
        {"_id": ticket_object_id},
        {"$set": ticket_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return {"message": "Ticket updated"}

@router.delete(
    "/{ticket_id}",
    response_model=MessageResponse
)
def delete_ticket(ticket_id: str):
    object_id = get_object_id(ticket_id)

    result = db.tickets.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return {"message": "Ticket deleted"}