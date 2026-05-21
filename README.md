# E-Commerce Serialization System

Simple educational e-commerce system written in Python.

The project demonstrates:
- OOP principles
- serialization/deserialization
- JSON storage
- enums
- encapsulation
- random fake data generation
- working with UUID
- simple order management system

---

# Features

## Product System
- Product categories
- Currency support
- Product stock management
- Product price management
- UUID product identifiers

## Customer System
- Customers with orders
- Order history
- Multiple orders per customer

## Order System
- Multiple products in one order
- Total price calculation

## JSON Serialization
- Save data to JSON
- Load data from JSON
- Empty/broken JSON handling

## Fake Data Generation
Using Faker library for:
- random customers
- random products
- random orders

---

# Technologies

- Python 3.12+
- Faker

---

# Project Structure

```bash
hillel_hw_4/
│
├── data/
│   └── ecom_data.json
│
├── models/
│   └── ecom_models.py
│
├── serialization/
│   └── json_serialization.py
│
├── fake_data.py
├── main.py
│
└── README.md
```

---

# Installation

Clone repository:

```bash
git clone https://github.com/OleksandrPiatnytsia/hillel_hw_4.git
```

Move to project directory:

```bash
cd hillel_hw_4
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

## Windows

```bash
venv\Scripts\activate
```

## Linux / MacOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run Project

```bash
python main.py
```

---

# Main Concepts Used

- Classes
- Encapsulation
- Properties
- Class methods
- Serialization
- UUID
- Type hints
- Enums
- Context managers
- File handling
- JSON
- Faker

---

# Example Product JSON

```json
{
    "id": "9bdbf3cc-c6ea-48e3-bf58-59d6dc9fd4b4",
    "title": "Teddy Bear",
    "category": "soft toy",
    "currency": "USD",
    "description": "Soft toy",
    "price": 25,
    "stock_quantity": [10, 5]
}
```

---

# Future Improvements

- SQLite/PostgreSQL support
- Product repository pattern
- Async support
- REST API
- Docker support
- Unit tests
- Logging
- Validation system

---

# Author

Oleksandr Piatnytsia

GitHub:
https://github.com/OleksandrPiatnytsia