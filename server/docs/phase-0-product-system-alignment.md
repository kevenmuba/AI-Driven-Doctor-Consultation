PHASE 0 – Product & System Alignment

(Before Writing Any Django Code)

🎯 Goal

Ensure all critical backend decisions are locked before implementation begins, so:

No schema rewrites

No auth confusion

No frontend–backend mismatch

No “we should have thought of this earlier”

This phase defines the contract for the entire system.

1️⃣ MVP Scope (Locked)
What this MVP WILL do

Patient describes symptoms (text)

AI suggests suitable doctor specialty

Patient requests appointment

Doctor accepts/rejects

Secure text chat after acceptance

Admin manages doctors

What this MVP WILL NOT do

No video calls

No payments

No prescriptions

No diagnosis automation

No medical file uploads

AI is decision support, not diagnosis.

✅ Scope is final for MVP.

2️⃣ User Roles & Permissions (Locked)
Roles
Role	Description
ADMIN	System owner, manages doctors
DOCTOR	Verified consultant
PATIENT	Person seeking consultation
Permission Rules

ADMIN:

Create & verify doctors

Activate/deactivate users

DOCTOR:

Accept/reject appointments

Chat with assigned patients

PATIENT:

Submit symptoms

Request appointments

Chat after approval

❗ No shared permissions
❗ No role switching in MVP

3️⃣ Database Schema (Locked)

Database: PostgreSQL

Schema defined in: db.sql

Schema principles:

Normalized

Role-based

Audit-friendly (AI decisions stored)

One appointment → one chat room

Core Tables

users

doctor_profiles

patient_profiles

doctor_availability

symptom_analyses

appointments

chat_rooms

messages

✅ Schema is final for MVP

4️⃣ Backend Architecture Decisions
🔐 Authentication

JWT-based authentication

Access token + refresh token

No session-based auth

Stateless backend

Reason:

Mobile-ready

Scales easily

Frontend friendly

🌐 API Style

REST API

JSON only

No server-side templates

No Django HTML rendering

Reason:

Clean frontend–backend separation

Works with web & mobile

🧭 API Versioning

All endpoints are versioned:

/api/v1/


Example:

POST /api/v1/auth/login
GET  /api/v1/doctors/


Reason:

Safe future evolution

No breaking frontend changes

5️⃣ Tooling Choices (Final)
Backend Framework

Django

Django REST Framework (DRF)

Why:

Mature

Secure

Excellent ecosystem

Fast MVP development

Database

PostgreSQL

Why:

Strong relational integrity

JSON support (future)

Production proven

Authentication

djangorestframework-simplejwt

Why:

Standard JWT implementation

Actively maintained

DRF-native

API Documentation

Swagger / OpenAPI

Access:

/api/docs/


Why:

Frontend consumes API without guessing

Acts as living documentation

Reduces meetings & confusion

6️⃣ High-Level System Diagram (Textual)
[ Frontend (Web / Mobile) ]
            |
            |  HTTPS (JWT)
            v
[ Django REST API ]
            |
            |
     ------------------
     |       |        |
 [Auth]  [AI Triage] [Appointments]
     |       |        |
   [Users] [Symptoms] [Chat]
            |
        [PostgreSQL]

7️⃣ API Style Guide (FIRST VERSION)

This is the contract with frontend.

General Rules

JSON only

Snake_case for backend fields

ISO 8601 dates

Meaningful HTTP status codes

HTTP Status Codes
Code	Meaning
200	Success
201	Created
400	Validation error
401	Unauthorized
403	Forbidden
404	Not found
409	Conflict
500	Server error
Error Response Format (Standard)
{
  "error": "VALIDATION_ERROR",
  "message": "Email already exists"
}

Auth Header
Authorization: Bearer <access_token>

Pagination (Default)
{
  "count": 120,
  "next": "/api/v1/appointments?page=2",
  "previous": null,
  "results": []
}

8️⃣ Phase 0 Deliverables (Final)

✅ db.sql
✅ Backend architecture decisions
✅ API style guide (v1)
✅ Role & permission rules
✅ System diagram

🔒 Phase 0 Exit Criteria

You DO NOT move to Phase 1 unless:

Schema is approved

Roles are final

Auth method is final

Frontend agrees with API style