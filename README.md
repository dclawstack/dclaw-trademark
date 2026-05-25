# DClaw Trademark

> **Trademark Management SaaS — powered by the DClaw Stack.**
> A vertical SaaS application for trademark search, filing, monitoring, and portfolio management.

## What This Is

**DClaw Trademark** is a domain-specific application built on the DClaw Stack:
- ✅ FastAPI backend with correct SQLAlchemy 2.0 setup
- ✅ Next.js 14 frontend with Tailwind + pre-built UI components
- ✅ Docker + docker-compose with working healthchecks
- ✅ Helm chart for Kubernetes deployment
- ✅ Alembic migrations setup
- ✅ pytest test harness with pinned pytest-asyncio==0.24.0
- ✅ GitHub Actions CI
- ✅ `AGENTS.md` + `PLAN-v1.2.md` templates
- ✅ Pre-built UI components (no shadcn CLI needed)

## App Identity

| Setting | Value |
|---------|-------|
| App Name | DClaw Trademark |
| Backend Port | **8066** (FastAPI) |
| Frontend Port | **3066** (Next.js) |
| Database | **dclaw_trademark** (PostgreSQL) |
| Base API Path | `/api/v1` |

## Contributors

| Name | Email | Role |
|------|-------|------|
| Rajendra Machani | 01.r.machani@gmail.com | Project Lead |

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/dclawstack/dclaw-trademark.git
cd dclaw-trademark

# 2. Copy env file
cp .env.example .env

# 3. Start with Docker
docker compose up -d

# Backend:  http://localhost:8066
# Frontend: http://localhost:3066
# API Docs: http://localhost:8066/docs
```

## Critical Rules for Agents

### DO NOT install shadcn CLI
The scaffold includes pre-built UI components in `frontend/src/components/ui/`. Installing `shadcn` v4 or `@base-ui/react` will break the Tailwind v3 build.

### DO NOT change the Postgres test port
`backend/tests/conftest.py` uses `localhost:5432`. GitHub Actions CI maps the Postgres service to port 5432. Changing this breaks CI.

### DO NOT delete `.github/workflows/ci.yml`
This file is required for GitHub Actions to run tests on every push.

### DO NOT upgrade pytest-asyncio
Keep `pytest-asyncio==0.24.0` pinned in `requirements.txt`. v1.3.0 breaks fixture scoping.

## Port Registry

| App | Backend Port | Frontend Port | Database |
|-----|-------------|---------------|----------|
| dclaw-chat | 8090 | 3000 | dclaw_chat |
| dclaw-med | 8092 | 3004 | dclaw_med |
| dclaw-learn | 8093 | 3003 | dclaw_learn |
| dclaw-code | 8094 | 3005 | dclaw_code |
| dclaw-legal | 8099 | 3013 | dclaw_legal |
| dclaw-crm | 8095 | 3006 | dclaw_crm |
| dclaw-finance | 8096 | 3007 | dclaw_finance |
| dclaw-hr | 8097 | 3008 | dclaw_hr |
| **dclaw-trademark** | **8066** | **3066** | **dclaw_trademark** |

> **Rule:** New apps take the next available port. Update this table when assigning.

## Files You Must Customize

| File | What to Change |
|------|---------------|
| `backend/app/core/config.py` | `app_name`, default database name |
| `backend/app/api/main.py` | Wire v1 routers |
| `frontend/package.json` | Package name |
| `frontend/src/app/layout.tsx` | Title, description |
| `frontend/src/app/page.tsx` | Dashboard content |
| `docker-compose.yml` | Port mappings |
| `helm/Chart.yaml` | Chart name |
| `helm/values.yaml` | Image repository names |
| `AGENTS.md` | App identity, port numbers |
| `PLAN-v1.2.md` | Feature backlog |
| `PRODUCT-SPEC.md` | (Create this) Domain models, business logic |

## What You Should NOT Change

- `app/models/base.py` — `DeclarativeBase` pattern
- `app/core/database.py` — Engine/session factory
- `docker-compose.yml` healthcheck commands
- `frontend/Dockerfile` `ARG NEXT_PUBLIC_API_URL` pattern
- `tests/conftest.py` — Test DB override pattern (keep `localhost:5432`)
- `frontend/src/components/ui/*.tsx` — Pre-built components (use as-is)
- `requirements.txt` — Keep `pytest-asyncio==0.24.0` pinned
- `.github/workflows/ci.yml` — Do not delete
