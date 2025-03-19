# FastAPI Backend Template

## Overview

This is a template backend project built with [FastAPI](https://fastapi.tiangolo.com/), designed for quick deployment and extension. It includes user authentication, JWT-based token management, and basic CRUD operations for posts, with MySQL as the database.

## Features

- **User Authentication**: Secure user registration and login using JWT tokens.
- **Post Management**: Create, retrieve, and delete posts associated with authenticated users.
- **Database Integration**: Utilizes MySQL for persistent data storage.
- **Automated Testing**: Test suite uses `pytest` and `httpx`

## Getting Started

### Prerequisites

- **Python 3.13** (may work with older versions but tested with `3.13`)
- **MySQL**
- **Redis**

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/qwadratic/python-api-template.git
   cd backend_project
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:

   Create a `.env` file in the `app/` directory with the following content:

   ```env
   DATABASE_URL=mysql+mysqlconnector://user:password@localhost/db_name
   SECRET_KEY=your_secret_key
   ```

   Replace `user`, `password`, `localhost`, and `db_name` with your MySQL credentials and desired database name.

5. **Apply Database Migrations**:

   If using Alembic for migrations, initialize and apply migrations:

   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

   Ensure the `alembic.ini` file is configured with your `DATABASE_URL`.

### Running the Application

Start the FastAPI application using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

Access the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Running Tests

Execute the test suite using `pytest`:

```bash
pytest -v
```

