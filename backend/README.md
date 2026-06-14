# Olympiad Competition Management System

Backend implementation of a programming olympiad competition management system built with Django and Django REST Framework.

## Tech Stack

* Python
* Django 4.x
* Django REST Framework
* JWT Authentication (SimpleJWT)
* SQLite
* Pytest
* drf-spectacular (OpenAPI)

---

# Features

## Authentication

* JWT-based authentication
* Access and Refresh tokens
* Protected API endpoints

## Participants

* Create participants
* List participants
* Unique email validation
* Grade validation

## Problems

* Create problems
* List problems
* Difficulty levels:

  * Easy
  * Medium
  * Hard

## Leaderboard

* Ordered by total score
* City filtering
* Pagination support
* Database-level aggregation using `annotate()` and `Sum()`
* No N+1 query issues

## Statistics

Leaderboard statistics endpoint provides:

* Participant count
* Average score
* Maximum score
* Minimum score
* Score distribution

---

# API Documentation

### Swagger UI

```text
/api/docs
```

### Schema

```text
/api/schema
```

### Redoc

```text
/api/redoc
```

---

# Running the Project

Start all services (it will automatically create an admin user with username=`admin` and password=`admin`):

```bash
docker compose -f development.yml up --build -d
```

---

# Running the Backend Without Docker

Apply migrations:

```bash
pip install -r .\requirements\development.txt
```

```bash
cd .\core\
python manage.py migrate
```

Create an admin user:

```bash
python manage.py create_admin_user
```

Seed sample data:

```bash
python manage.py seed_olympiad
```

Start the development server:

```bash
python manage.py runserver
```

---

# Default Admin Credentials

```text
Username: admin
Password: admin
```

---

# Management Commands

## Create Admin User

Creates a default administrator account.

```bash
python manage.py create_admin_user
```

---

## Seed Sample Data

This command creates sample data for testing and demonstration purposes.

```bash
python manage.py seed_olympiad
```

Creates:

* Participants
* Problems
* Submissions

Useful for testing leaderboard and statistics endpoints.

---

# Running Tests

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest path/to/test_file.py
```

---

# API Endpoints

## Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/login/refresh/
```

## Participants

```http
GET  /api/participants/
POST /api/participants/
```

## Problems

```http
GET  /api/problems/
POST /api/problems/
```

## Submissions

```http
POST /api/submissions/
```

## Leaderboard

```http
GET /api/leaderboard/
```

Filter by city:

```http
GET /api/leaderboard/?city=Tehran
```

Pagination:

```http
GET /api/leaderboard/?page=1&page_size=10
```

## Statistics

```http
GET /api/leaderboard/stats/
```

---

# Design Decisions

* A custom user model is used for authentication.
* Participants are domain entities and are not authenticated users.
* Database constraints are used to enforce data integrity.
* Leaderboard calculations are performed at the database level using Django ORM aggregations.
* The implementation avoids N+1 query issues.
* Business rules are enforced both at the serializer layer and the database layer where appropriate.

---

# Notes

* Only administrators authenticate and interact with the system.
* Leaderboard ranking is calculated based on the sum of final submission scores.
* For each participant/problem pair, only one submission can be marked as final (`is_final=True`).
* When a new submission is created for the same participant and problem, the previous final submission is automatically marked as non-final.
