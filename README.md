# RetailFlow - An Ecommerce and Inventory Management System

RetailFlow is a Django-based retail management and e-commerce application designed to manage products, categories, suppliers, inventory, shopping carts, customer orders, and order processing.

The project also provides a REST API using Django REST Framework with authentication, role-based permissions, filtering, searching, ordering, pagination, validation, and secure order processing.

> 🚧 **Development Status:** RetailFlow is an actively evolving project. Core backend functionality and REST API features have been implemented, while additional technologies, features, UI improvements, testing, and deployment capabilities are being progressively added.

---

## 📌 Project Overview

RetailFlow is being developed as a practical full-stack retail management system that combines:

- Customer-facing e-commerce functionality
- Inventory management
- Supplier management
- Order processing
- Role-based access control
- REST API services
- Transaction-safe stock management
- Docker-based development

The goal is to progressively evolve the application into a more complete, production-oriented retail management and e-commerce platform.

---

## ✨ Features

### 👤 Customer Features

- User registration
- User login and logout
- Browse products
- Search products
- Filter products by category
- Sort products
- Add products to cart
- Increase quantity when adding an existing product
- Update cart quantities
- Remove products from cart
- Checkout
- Automatic order creation
- Automatic inventory deduction
- View order history
- View individual order details
- Track order status

### 👨‍💼 Staff / Admin Features

Authorized staff and administrators can manage:

- Products
- Categories
- Suppliers
- Inventory
- Customer orders
- Order status

Access to management operations is controlled through role-based permissions.

---

## 🛒 Order Processing

RetailFlow implements a transaction-safe checkout workflow.

When a customer places an order:

1. The customer's cart is retrieved.
2. A database transaction is started.
3. The required inventory records are locked.
4. Stock availability is checked.
5. Order items are created.
6. Inventory quantities are reduced.
7. The order total is calculated.
8. The order is saved.
9. The customer's cart is cleared.

If an error occurs during the process, the transaction is rolled back.

This helps prevent inconsistent order and inventory data.

---

## 📦 Inventory Management

The inventory system maintains:

- Available stock quantity
- Reorder level
- Product association
- Inventory update timestamp

Inventory is automatically reduced when a customer successfully completes checkout.

Stock availability is checked before an order is created.

---

## 🚚 Order Status Workflow

Orders follow a controlled status workflow:

```text
PENDING
   │
   ▼
CONFIRMED
   │
   ▼
PROCESSING
   │
   ▼
SHIPPED
   │
   ▼
DELIVERED

🔐 Authentication & Authorization
RetailFlow implements authentication and role-based access control.
Customer
Customers can:
- Browse products
- Manage their own cart
- Place orders
- View their own orders
Customers cannot:
- Modify products
- Modify inventory
- Modify suppliers
- Change order status
- Modify protected order fields
Staff / Admin
Authorized staff and administrators can perform management operations such as:
- Product management
- Category management
- Supplier management
- Inventory management
- Order status updates

🌐 REST API
RetailFlow provides REST APIs using Django REST Framework.
Base API path:
/api/

API Resources
/api/products/
/api/categories/
/api/suppliers/
/api/inventory/
/api/cart/
/api/orders/

API Capabilities
The API includes:
- Authentication
- Role-based permissions
- CRUD operations
- Validation
- Pagination
- Search
- Filtering
- Ordering
- Protected customer resources
- Controlled order status updates
Example
GET /api/products/

The product API supports:
- Product listing
- Product retrieval
- Product creation
- Product updates
- Product deletion
- Search
- Category filtering
- Ordering
- Pagination
🔎 API Filtering, Searching & Ordering
The product API supports filtering and searching.
Examples:
/api/products/?search=laptop

/api/products/?category=1

Ordering can be performed using supported product fields.
Pagination is also enabled for API responses.
🗄️ Database Design
RetailFlow uses PostgreSQL as its relational database.
Main Models

Category
Stores product category information.

Product
Stores:
- Product name
- Description
- MRP
- Selling price
- Expiry date
- Category
- Creation timestamp
- Update timestamp

Supplier
Stores:
- Supplier name
- Email
- Phone
- Address
- Creation timestamp

ProductSupplier
Associates products with suppliers and stores supply prices.
A product-supplier relationship is uniquely maintained.
Inventory
Maintains:
- Product
- Stock quantity
- Reorder level
- Update timestamp

CartItem
Represents products added to a customer's cart.
A customer cannot have duplicate cart entries for the same product. Adding the same product again increases its quantity.
Order
Stores:
- Customer
- Order status
- Total amount
- Creation timestamp
- Update timestamp

OrderItem
Stores:
- Order
- Product
- Quantity
- Price at the time of order

🧩 Project Structure
RetailFlow/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── urls.py
│   └── views.py
│
├── api/
│   ├── migrations/
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── orders/
│   ├── migrations/
│   ├── services.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── products/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── RetailFlow/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
├── templates/
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md

🛠️ Technology Stack
Backend
- Python
- Django
- Django REST Framework
Database
- PostgreSQL
Frontend
- HTML
- CSS
- JavaScript
- Django Templates
API
- Django REST Framework
- Django Filter
Development & Tools
- Git
- GitHub
- Visual Studio Code

🚀 Local Development Setup
1. Clone the repository
git clone <your-github-repository-url>
cd RetailFlow

2. Create a virtual environment
python -m venv venv

Windows
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables
Create a .env file.
Example:
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True

DB_NAME=RetailMate
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

Never commit the .env file containing real secrets or database credentials.

5. Apply migrations
python manage.py migrate

6. Run the development server
python manage.py runserver

Open:
http://127.0.0.1:8000/


✅ Completed
- Django project structure
- PostgreSQL integration
- Database models and relationships
- User authentication
- Customer / Staff access control
- Product management
- Category management
- Supplier management
- Inventory management
- Shopping cart
- Checkout
- Transaction-safe inventory deduction
- Order management
- Order status workflow
- REST API
- API authentication and permissions
- API pagination
- API search
- API filtering
- API ordering
- Input validation
- Query optimization
- API security testing
- Django security configuration
- Database migration audit
- Docker setup
- Docker Compose configuration

🔄 Currently Being Developed
- Docker configuration
- Reliable container startup
- Production-oriented application serving
- Static file configuration
- Complete e-commerce UI redesign
- Additional automated tests
- Full end-to-end testing

🔮 Planned / Upcoming
Additional technologies and capabilities will be progressively integrated as development continues.
Planned areas include:
- Production deployment
- Production application server
- Improved responsive e-commerce interface
- Additional testing
- CI/CD improvements
- Monitoring and deployment improvements
- Other relevant technologies as the project evolves
Note: Technologies and features listed as planned are not represented as completed functionality.

🎯 Project Goals
The long-term goal of RetailFlow is to develop a practical, production-oriented retail management and e-commerce platform demonstrating skills in:
- Backend development
- Full-stack web development
- REST API development
- Database design
- Authentication and authorization
- Inventory management
- Transaction handling
- API security
- Query optimization
- Containerization
- Deployment
- Software testing

📚 What This Project Demonstrates
RetailFlow demonstrates practical experience with:
- Building a Django application from the ground up
- Designing relational database models
- Implementing business workflows
- Developing REST APIs
- Implementing role-based permissions
- Handling inventory safely during checkout
- Working with PostgreSQL
- Optimizing Django ORM queries
- Writing automated tests
- Containerizing applications with Docker
- Managing application configuration using environment variables
- Using Git and GitHub for version control

👨‍💻 Author
Ravi Sankar Reddy Veluri
B.Tech – Electronics and Communication Engineering
Interests
- Python Development
- Django
- Backend Development
- Full Stack Development
- REST API Development
- SQL & Databases

📌 Project Status
RetailFlow — Active Development 🚧
The project is continuously being improved with new technologies, features, testing, UI enhancements, and deployment capabilities.
More updates will be added as development progresses.
```
