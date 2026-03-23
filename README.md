# TaskMaster Backend (Django REST API)

This repository is the backend (middleware + persistence layer) for a small Task Management Application.

It is intentionally kept small, but follows a clean architecture style so it is easy to explain in an assignment demo.

## What This Project Covers

- User registration
- User login using JWT tokens
- Protected API endpoints
- One domain CRUD feature: personal task management
- Server-side validation and basic business rules
- Unit/API tests for key flows

## Tech Stack

- Django
- Django REST Framework
- Simple JWT (token auth)
- PostgreSQL (production) or SQLite (local dev)

## Architecture (3 Layers)

1. Frontend layer (separate React repo)
2. Middleware layer (this Django REST API)
3. Database layer (PostgreSQL in deployment)

Important rule: frontend talks only to API, never directly to database.

## Project Structure

```
django_taskmaster_backend/backend/
	backend/
		settings.py        # environment config, DRF, JWT, DB
		urls.py            # project URL routing
	taskmaster_mitten/
		models.py          # Task model
		serializers.py     # request/response + validation
		permissions.py     # ownership access control
		services.py        # task filtering/search logic
		views.py           # API views
		urls.py            # app-level API routes
		tests.py           # auth + task API tests
```

## Domain Model

`Task`
- `owner` (FK to user)
- `title`
- `description`
- `status` (`todo`, `in_progress`, `done`)
- `due_date`
- `created_at`, `updated_at`

## Business Rules Implemented

1. Task title must be at least 3 characters.
2. `due_date` cannot be in the past unless task is already `done`.
3. To mark a task as `done`, description must be meaningful (10+ characters).
4. Users can only access their own tasks.

## Setup (Local)

### 1. Go into backend folder

```bash
cd django_taskmaster_backend/backend
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run dev server

```bash
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## API Endpoints

### Authentication

- `POST /api/auth/register/`
- `POST /api/auth/login/` (returns `access` and `refresh`)
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/` (protected)

### Tasks (Protected)

- `GET /api/tasks/` (list own tasks)
- `POST /api/tasks/` (create task)
- `GET /api/tasks/<id>/` (retrieve own task)
- `PATCH /api/tasks/<id>/` (update own task)
- `DELETE /api/tasks/<id>/` (delete own task)

Optional query params on list:
- `status=todo|in_progress|done`
- `q=<text>` (search title/description)

## Example Auth Flow

1. Register user
2. Login and copy `access` token
3. Send header on protected routes:

```http
Authorization: Bearer <access_token>
```

## Testing

Run:

```bash
python manage.py test
```

Current tests cover:
- registration works
- task endpoints require auth
- authenticated user can create task
- business-rule validation for done tasks
- users cannot access another user's tasks

## Deployment Notes (Render-ready)

Set environment variables in deployment platform:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=<your-domain>`
- `CORS_ALLOWED_ORIGINS=<frontend-url>`
- `DATABASE_URL=<postgres-connection-string>`

Use PostgreSQL in production. This project supports `DATABASE_URL` format out of the box.

## Suggested Demo Script (for video)

1. Register a user
2. Login and show JWT response
3. Create a task
4. Update task status
5. Try accessing another user's task (show 403)
6. Run tests quickly in terminal
7. Show deployment URL and working API route

## Why This Is “Small but Enterprise-style”

- Clear layer separation (frontend/API/database)
- Auth and protected routes
- Modular backend files (views, serializers, services, permissions)
- Business rules in server-side validation
- Tests for core flows
- Environment-based config for deployment