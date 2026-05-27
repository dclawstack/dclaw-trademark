# DClaw Trademark — Development Checklist
*Branch: `claude/post-merge-dev-tasks-2` | Updated: 2026-05-26*

---

## Pre-Flight Checklist

- [x] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [x] `frontend/next-env.d.ts` exists and is committed
- [x] `docker-compose.yml` healthchecks correct (python urllib backend, wget frontend)
- [x] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`
- [x] All alembic migrations generated (`9f9cd1759abb_initial_schema`, `8ea3e1140795_add_opposition_search_query_subscription`)
- [x] `pytest` passes before pushing (55/55 passing)
- [x] Fix pydantic v2 deprecation warning in `backend/app/core/config.py`

---

## Complexity 0 — Foundation (Sprint 1)

- [x] **C0.1** Trademark Core Model (`backend/app/models/trademark.py`)
- [x] **C0.2** Nice Classification Model — `TrademarkClass` in `trademark.py`
- [x] **C0.3** Watchlist & Deadline Models (`watchlist.py`, `deadline.py`)
- [x] **C0.4** Trademark CRUD API (`api/v1/trademarks.py`, schemas, repo)
- [x] **C0.5** Watchlist & Deadline CRUD APIs (`api/v1/watchlist.py`, `deadlines.py`)
- [x] **C0.6** Alembic Initial Migration — `backend/alembic/versions/9f9cd1759abb_initial_schema.py`
- [x] **C0.7** DPanel Manifest — `frontend/public/dclaw-manifest.json`
- [x] **C0.8** Portfolio UI + Trademark Detail (`portfolio/page.tsx`, `portfolio/[id]/page.tsx`)
- [x] **C0.9** Backend Tests — trademarks, watchlist, deadlines, health

---

## Complexity 1 — Core Differentiators (Sprint 2–4)

- [x] **C1.1** Nice Classification Service (`services/nice_classes.py`, `GET /api/v1/classes`)
- [x] **C1.2** Trademark Search — Phase A mock + Phase B USPTO adapter (`services/clearance_search.py`)
- [x] **C1.3** Phonetic + Semantic Similarity Scoring (`services/similarity.py`)
- [x] **C1.4** Deadline Alert Engine (`services/deadline_engine.py`, `GET /api/v1/deadlines/upcoming`)
- [x] **C1.5** AI Class Recommendation (`services/class_recommender.py`, `POST /api/v1/ai/suggest-classes`)
- [x] **C1.6** AI Trademark Copilot (`services/copilot.py`, `POST /api/v1/ai/copilot/chat`, `TrademarkCopilot.tsx`)
- [x] **C1.7** Watch Service Dashboard (`frontend/src/app/watchlist/page.tsx`)
- [x] **C1.8** Search UI (`frontend/src/app/search/page.tsx`)
- [x] **C1.x** Tests for C1 endpoints (classes, search, AI)

---

## Complexity 2 — Advanced Features (Sprint 5–6)

- [x] **C2.1** Enhanced Copilot / Search Audit — `search_queries` audit log wired into clearance search
- [x] **C2.2** USPTO Registry Adapter — `services/registries/uspto.py`; live TSDR call + fixture fallback
- [x] **C2.3** Background Scheduler — `services/scheduler.py`; APScheduler with 24h watch scan + 6h deadline check
- [x] **C2.4** AI Application Drafting — `services/application_drafter.py`, `POST /api/v1/ai/draft-application`
- [x] **C2.5** Logo Search Stub — `POST /api/v1/ai/search/logo` (v1.4 roadmap stub; MinIO+CLIP needed for full impl)
- [x] **C2.6** Opposition & Enforcement Tracking — `models/opposition.py`, `api/v1/oppositions.py`, `frontend/src/app/oppositions/page.tsx`
- [x] **C2.7** Stripe Billing — `models/subscription.py`, `api/v1/billing.py`, `frontend/src/app/billing/page.tsx`
- [ ] **C2.8** Multi-Tenant Architecture — deferred; requires Logto JWT middleware + row-level policy
- [x] **C2.x** Tests for C2 features (55/55 passing: +oppositions, +billing, +ai_draft)
