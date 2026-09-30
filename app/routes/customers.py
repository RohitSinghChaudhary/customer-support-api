from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from app.database import db
from app.models import (
    Customer,
    CustomerListResponse,
    CustomerResponse,
    IDResponse,
    MessageResponse
)

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_object_id(customer_id: str):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid customer ID"
        )
    return ObjectId(customer_id)

def serialize_customer(customer):
    return {
        "id": str(customer["_id"]),
        "name": customer["name"],
        "email": customer["email"]
    }

@router.post(
    "",
    response_model=IDResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(customer: Customer):
    result = db.customers.insert_one(customer.model_dump())
    return {
        "message": "Customer created",
        "id": str(result.inserted_id)
    }

@router.get(
    "",
    response_model=CustomerListResponse
)
def get_customers():
    customers = [
        serialize_customer(customer)
        for customer in db.customers.find()
    ]
    return {"customers": customers}

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(customer_id: str):
    object_id = get_object_id(customer_id)
    customer = db.customers.find_one({"_id": object_id})

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return serialize_customer(customer)

@router.put(
    "/{customer_id}",
    response_model=MessageResponse
)
def update_customer(customer_id: str, customer: Customer):
    object_id = get_object_id(customer_id)

    result = db.customers.update_one(
        {"_id": object_id},
        {"$set": customer.model_dump()}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {"message": "Customer updated"}

@router.delete(
    "/{customer_id}",
    response_model=MessageResponse
)
def delete_customer(customer_id: str):
    object_id = get_object_id(customer_id)

    ticket_count = db.tickets.count_documents(
        {"customer_id": object_id}
    )

    if ticket_count > 0:
        raise HTTPException(
            status_code=409,
            detail="Customer has existing tickets and cannot be deleted"
        )

    result = db.customers.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {"message": "Customer deleted"}