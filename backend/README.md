# Kids Pixel Pals Backend

FastAPI backend for the Kids Pixel Pals safe social platform for children.

## Features

- **Parent-First Registration**: Closed-circle authentication with admin approval
- **Role-Based Access Control**: ADMIN, PARENT, CHILD roles with proper permissions
- **Secure Data Storage**: AES-256 encryption for sensitive data
- **JWT Authentication**: Short-lived access tokens with refresh tokens
- **Real-time Ready**: WebSocket support for chat and calls
- **Audit Logging**: Comprehensive logging of sensitive actions

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy 2.0** - ORM and database toolkit
- **Pydantic v2** - Data validation and serialization
- **JWT** - JSON Web Tokens for authentication
- **Argon2** - Secure password hashing
- **AES-256** - Encryption for sensitive data

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis (for real-time features)

### Installation

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your database credentials and secrets

6. Initialize database:
   ```bash
   alembic upgrade head
   ```

7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── routes/        # Route handlers
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── core/          # Core components
│   └── dependencies/  # FastAPI dependencies
├── tests/             # Test suite
├── migrations/        # Database migrations
└── scripts/           # Utility scripts
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Security Features

- **Closed Registration**: No public signup, parent-first with admin approval
- **Role Enforcement**: Strict RBAC at route and data levels
- **Data Encryption**: Sensitive fields encrypted at rest
- **Secure Cookies**: HttpOnly, Secure, SameSite cookies for refresh tokens
- **Rate Limiting**: Protection against brute force attacks
- **Audit Logs**: Immutable record of sensitive actions

## License

This project is part of the Kids Pixel Pals platform.