# OpsFlow

A modern service-business operations platform built as a senior-level Angular and FastAPI portfolio project.

## Product capabilities

- Angular 22 standalone application with Signals
- Responsive light/dark operational dashboard
- Searchable service-ticket workflow with inline status transitions
- FastAPI versioned API with typed responses, CORS and centralized errors
- Docker-ready API and PostgreSQL development environment
- Frontend and backend smoke tests
- JWT authentication with Argon2 password hashing and role enforcement
- Customer CRM, team directory, inventory control, invoices and payment recording
- Live operational KPIs, executive reports and print-friendly reporting
- Create workflows with validation, loading, empty, toast and error states
- Seeded demo workspace and live Angular API integration with offline fallback
- GitHub Actions, Render and Vercel deployment configuration

## Demo account

- Email: admin@opsflow.dev
- Password: OpsFlow123!
- API docs: http://localhost:8000/docs

## Production deployment

- Frontend: Vercel, root directory frontend
- Backend: Render Blueprint using render.yaml
- Database: Supabase PostgreSQL
- Set Render DATABASE_URL to the Supabase pooled connection string (Transaction mode, port 6543) and append `?ssl=require`.
- Vercel production and preview domains are accepted by the configured CORS regex.
- Production API: https://opsflow-api-81vr.onrender.com/api/v1
- PostgreSQL tables have RLS enabled automatically, preventing accidental direct access through Supabase's public Data API.

## Run frontend

    cd frontend
    npm install
    npm start

Open http://localhost:4200.

## Run API

    cd backend
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

Open http://localhost:8000/docs.

## Architecture

- Feature-oriented Angular UI using Signals and a typed API client
- Versioned FastAPI REST endpoints with JWT authentication and role guards
- SQLAlchemy async persistence for SQLite development and Supabase PostgreSQL production
- Row Level Security enabled for Supabase Data API isolation
- Dockerized Render backend, Vercel SPA deployment and GitHub Actions CI

## Portfolio scope

OpsFlow is a complete portfolio MVP. Enterprise extensions such as multi-tenant billing, external payment gateways, object storage and real-time notifications are intentionally outside the free-hosting demo scope.
