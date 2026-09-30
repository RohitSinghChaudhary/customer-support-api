# Customer Support API

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MongoDB Atlas](https://img.shields.io/badge/MongoDB_Atlas-47A248?logo=mongodb&logoColor=white)

A RESTful backend API for managing customers and their support tickets, built with **FastAPI** and **MongoDB Atlas**.

## Features

- Full CRUD operations for customers and support tickets
- Customer–ticket relationship validation, so tickets are tied to valid customers
- Request validation with Pydantic
- Error handling for invalid IDs and missing resources
- Interactive API documentation with Swagger UI

## Tech Stack

| Technology | Purpose |
|------------|---------|
| [Python](https://www.python.org/) | Programming language |
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [MongoDB Atlas](https://www.mongodb.com/atlas) | Cloud-hosted database |
| [PyMongo](https://pymongo.readthedocs.io/) | MongoDB driver for Python |
| [Pydantic](https://docs.pydantic.dev/) | Data validation and schemas |

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A [MongoDB Atlas](https://www.mongodb.com/atlas) cluster and its connection string

### Installation

1. **Clone the repository**

```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
```

2. **Create and activate a virtual environment** (recommended)

```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
   pip install -r requirements.txt
```

4. **Configure environment variables**

   Create a `.env` file in the project root and add your MongoDB connection string:

```env
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

5. **Start the server**

```bash
   fastapi dev app/main.py
```

The API is now running at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/customers` | Create a customer |
| `GET` | `/customers` | Get all customers |
| `GET` | `/customers/{customer_id}` | Get a customer by ID |
| `PUT` | `/customers/{customer_id}` | Update a customer |
| `DELETE` | `/customers/{customer_id}` | Delete a customer |

### Tickets

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tickets` | Create a support ticket |
| `GET` | `/tickets` | Get all tickets |
| `GET` | `/tickets/{ticket_id}` | Get a ticket by ID |
| `PUT` | `/tickets/{ticket_id}` | Update a ticket |
| `DELETE` | `/tickets/{ticket_id}` | Delete a ticket |

## Example Requests

You can try these directly from Swagger UI.

**Create a customer** — `POST /customers`

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Create a ticket** — `POST /tickets`

```json
{
  "customer_id": "<customer-id>",
  "title": "Unable to log in",
  "description": "The password reset email is not arriving.",
  "status": "open"
}
```

## Project Structure

```
.
├── app/
│   ├── main.py            # FastAPI app and router registration
│   ├── database.py        # MongoDB connection setup
│   ├── models.py          # Pydantic models
│   └── routes/
│       ├── customers.py   # Customer endpoints
│       └── tickets.py     # Ticket endpoints
├── requirements.txt
├── .gitignore
└── README.md
```

## Security

- The MongoDB connection string is stored in `.env`, which is excluded from Git via `.gitignore`.
- Never commit credentials. If a connection string is ever exposed, rotate the database user's password in MongoDB Atlas right away.

## Future Improvements

- [ ] Pagination and filtering (e.g. tickets by status or customer)
- [ ] Authentication and authorization
- [ ] Automated tests with pytest
- [ ] Docker support
