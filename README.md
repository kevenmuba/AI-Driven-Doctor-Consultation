# AI-Driven-Doctor-Consultation

📝 Backend & API Project — README
1️⃣ Overview

This repository contains the backend server for the Healthcare Platform.

The backend is built using Django + DRF and exposes REST APIs.

JWT authentication is used for secure, role-based access.

API endpoints are versioned under:

/api/v1/


Swagger documentation is available at:

http://localhost:8000/api/docs/


This README describes the server structure, its purpose, and guidelines for frontend integration (to be implemented in a client folder later).

2️⃣ Folder Structure (Server)
server/           # Backend code
├── config/       # Django project settings & urls
├── users/        # User management (authentication, roles, profiles)
├── doctors/      # Doctor profiles and availability
├── patients/     # Patient profiles
├── appointments/ # Appointment requests, status, linking AI
├── ai_triage/    # AI-assisted doctor recommendation
├── chat/         # Chat system between users and doctors
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

Highlights

models.py → database schema (users, doctors, patients, etc.)

serializers.py → data validation and serialization

services.py → business logic (keeps views thin)

views.py → API endpoints (controllers)

urls.py → routes for each app

Swagger/OpenAPI → live API documentation

The service layer is key: it centralizes business logic so both views and future scripts/cron jobs can reuse it.

3️⃣ Server Folder Purpose

Handles all business logic and data operations

Provides secure, role-based APIs

Supports admin, doctor, and patient roles with proper access controls

Includes testing & validation to ensure stability

Dockerized for easy deployment and environment consistency

4️⃣ Environment Setup (Server)
Prerequisites

Docker & Docker Compose installed

.env file with environment variables:

Variable	Description
DEBUG	Django debug mode (True/False)
SECRET_KEY	Django secret key
DB_NAME	PostgreSQL database name
DB_USER	PostgreSQL user
DB_PASSWORD	PostgreSQL password
DB_HOST	Docker service name (db)
DB_PORT	PostgreSQL port
OPENAI_API_KEY	AI integration key (optional)
Commands
# Build and run containers
docker compose up --build

# Apply migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

5️⃣ API Documentation & Testing

Swagger available at:

http://localhost:8000/api/docs/


Frontend developers can:

See all endpoints

Check request/response schema

Test endpoints interactively

Authorize via JWT tokens

Swagger serves as the primary frontend contract, reducing the need for separate API docs.

6️⃣ Frontend Integration (Future Client Folder)

The client folder will consume these APIs

Frontend developers will:

Use endpoints under /api/v1/

Pass JWT token in Authorization: Bearer <token> header

Handle role-based UI based on role in user profile

Once client folder is created, this README will be updated with frontend instructions, folder structure, and build steps.

7️⃣ Testing & Quality Assurance

Unit tests → services

API tests → views

Permission tests → role-based endpoints

Edge cases → invalid requests, missing fields

Load sanity tests → optional

# Run all tests
docker compose exec web python manage.py test

8️⃣ Deployment Notes

Dockerized for local, staging, and production

Use environment variables for configuration

Ensure DEBUG=False in production

Configure logging, monitoring, and security headers

API documentation (/api/docs/) should be publicly available for developers or internal only depending on environment

9️⃣ Key Principles

Service layer first: always use services for logic

Swagger first: API docs are the contract

Role-based design: ADMIN, DOCTOR, PATIENT

Dockerized: consistent dev/staging/prod environments

Future-proof: designed to integrate with frontend client seamlessly