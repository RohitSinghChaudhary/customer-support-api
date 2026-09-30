from fastapi import FastAPI

from app.routes.customers import router as customers_router
from app.routes.tickets import router as tickets_router

app = FastAPI(
    title="Customer Support API",
    version="0.1.0"
)

@app.get("/test")
def test():
    return {"message": "Customer Support API is running"}

app.include_router(customers_router)
app.include_router(tickets_router)