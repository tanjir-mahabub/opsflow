# OpsFlow

A modern service-business operations platform built as a senior-level Angular and FastAPI portfolio project.

## Current foundation

- Angular 22 standalone application with Signals
- Responsive light/dark operational dashboard
- Searchable service-ticket table and KPI analytics
- FastAPI versioned API with typed responses, CORS and centralized errors
- Docker-ready API and PostgreSQL development environment
- Frontend and backend smoke tests

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

## Delivery roadmap

1. Authentication, tenant isolation and RBAC
2. Customers, technicians and service-ticket workflow
3. Inventory, invoices, payments and file storage
4. Audit trail, WebSocket notifications and rule-based insights
5. Accessibility, E2E coverage, CI and deployment
