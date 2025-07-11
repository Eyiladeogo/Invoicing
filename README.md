# Small Business Invoicing Backend

This project is a simplified backend for a small business invoicing tool, built with Django and Django REST Framework. It provides a RESTful API to manage customers, create invoices with multiple line items, and track invoice statuses.

## Features

- **Customer Management:** Create and list customers.
- **Invoice Creation:** Issue invoices to customers with multiple, nested line items in a single request.
- **Detailed Invoice View:** Retrieve full details of an invoice, including all its items and an automatically calculated total amount.
- **Status Updates:** Partially update an invoice to modify its status (e.g., from "pending" to "paid").
- **Data Validation:** Ensures data integrity, such as preventing an invoice's due date from being before its issue date or creating an invoice without line items.

---

## Project Setup

To get this project running locally, follow these steps:

### 1. Clone the Repository

```sh
git clone https://github.com/Eyiladeogo/Invoicing
cd invoicing_project
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

#### macOS/Linux

```sh
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```sh
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Then, run the installation command:

```sh
pip install -r requirements.txt
```

### 4. Run Database Migrations

This will create the necessary database tables based on the models defined in the `api` app.

```sh
python manage.py migrate
```

### 5. Run the Development Server

```sh
python manage.py runserver
```

The API will now be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## API Endpoints

All endpoints are prefixed with `/api/`.

| Method | Endpoint        | Description                                  |
| ------ | --------------- | -------------------------------------------- |
| POST   | /customers/     | Creates a new customer                       |
| GET    | /customers/     | Lists all existing customers                 |
| POST   | /invoices/      | Creates a new invoice with nested line items |
| GET    | /invoices/<id>/ | Retrieves a single invoice with its items    |
| PATCH  | /invoices/<id>/ | Updates an invoice (e.g., to change status)  |

---

## Request & Response Examples

### 1. Create a Customer

**Request:**

`POST /api/customers/`

```json
{
  "name": "Peter Parker",
  "email": "peterparker@marvel.com"
}
```

### 2. Create an Invoice

**Request:**

`POST /api/invoices/`

```json
{
  "customer": 1,
  "issue_date": "2025-07-15",
  "due_date": "2025-08-15",
  "items": [
    {
      "description": "Web Shooters",
      "quantity": 10,
      "unit_price": "50.00"
    },
    {
      "description": "Spidey Suit",
      "quantity": 1,
      "unit_price": "20.00"
    }
  ]
}
```

**Successful Response (201 Created):**

```json
{
  "id": 1,
  "customer": 1,
  "issue_date": "2025-07-15",
  "due_date": "2025-08-15",
  "status": "pending",
  "items": [
    {
      "id": 1,
      "description": "Web Shooters",
      "quantity": 10,
      "unit_price": "50.00",
      "total": "500.00"
    },
    {
      "id": 2,
      "description": "Spidey Suit",
      "quantity": 1,
      "unit_price": "20.00",
      "total": "20.00"
    }
  ],
  "total_amount": "520.00"
}
```

### 3. Update an Invoice Status

**Request:**

`PATCH /api/invoices/1/`

```json
{
  "status": "paid"
}
```

---

## Running Tests

The project includes a basic test suite to verify core functionality. To run the tests, use the following command:

```sh
python manage.py test
```
