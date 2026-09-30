from typing import Literal
from pydantic import BaseModel, EmailStr, Field, field_validator

class Customer(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value

class Ticket(BaseModel):
    customer_id: str
    subject: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2000)
    status: Literal["open", "in_progress", "closed"] = "open"

    @field_validator("subject", "description")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value

class CustomerResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

class TicketResponse(BaseModel):
    id: str
    customer_id: str
    subject: str
    description: str
    status: Literal["open", "in_progress", "closed"]

class CustomerListResponse(BaseModel):
    customers: list[CustomerResponse]

class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]

class IDResponse(BaseModel):
    message: str
    id: str

class MessageResponse(BaseModel):
    message: str