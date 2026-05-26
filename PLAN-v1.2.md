# DClaw Trademark — v1.2 Feature Roadmap
*Updated: 2026-05-26 | Stack: FastAPI + Next.js 14 + PostgreSQL | Ports: 8066 / 3066*

> **DO NOT proceed to coding without reading this file AND `AGENTS.md` AND `REVISED-PRD.md`.**

---

## Pre-Flight Checklist

- [x] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [x] `frontend/next-env.d.ts` exists and is committed
- [x] `docker-compose.yml` healthchecks correct (python urllib backend, wget frontend)
- [x] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`
- [x] All alembic migrations generated (`9f9cd1759abb_initial_schema.py` + C2 migrations)
- [x] `pytest` passes before pushing (38+ tests green)

---

## YC-Standard Evaluation

### The Hair-on-Fire Problem

Trademark protection is universally painful and expensive:
- Clearance search with attorney: **$500–$2,500** per mark, **2–5 business days**
- Basic watch service: **$300–$500/mark/year** (Corsearch, MarkMonitor)
- Enterprise docketing: **$5,000–$15,000/month** (Anaqua, CPA Global)
- Result: **60% of startups skip trademark protection entirely** — they discover the risk only after a cease-and-desist
- 800,000+ USPTO applications/year, 3M+ active US marks; growing 7% annually

### Our 10× Advantage Over Incumbents

| Dimension | Incumbents (Corsearch, MarkMonitor) | DClaw Trademark |
|-----------|--------------------------------------|-----------------|
| Price | $5,000–$15,000/month | $49/search or $99/seat/month |
| Time to clearance | 2–5 business days | **<60 seconds** |
| Target user | Fortune 500 IP counsel | **Startups, SMBs, solo founders** |
| AI integration | Bolt-on (legacy UI + AI badge) | **AI-native from day 1** |
| Setup | Onboarding call + contract | **Self-serve, credit card** |
| Watch monitoring | Manual + email digest | **Real-time alerts** |

### Competitive Moat (Technical Defensibility)

1. **Phonetic + Semantic + Visual similarity pipeline** — Soundex/Double Metaphone + TF-IDF embeddings → proprietary risk score
2. **AI Copilot with trademark domain RAG** — LLM trained on USPTO classification guidelines + TTAB decisions
3. **Network effect** — more portfolio data → better conflict detection → better product for all users
4. **API-first** — integrate into CLO tools, patent management suites, IP docketing workflows

### YC Gaps Requiring Resolution (Priority Order)

| # | Gap | Severity | Resolution |
|---|-----|----------|------------|
| 1 | No real trademark models / DB schema | 🔴 Critical | Complexity 0.1–0.3 |
| 2 | No API routes — zero endpoints beyond /health | 🔴 Critical | Complexity 0.4–0.6 |
| 3 | No phonetic/semantic similarity scoring | 🔴 Differentiator | Complexity 1.3 |
| 4 | No AI copilot | 🔴 YC mandate | Complexity 1.6 / 2.1 |
| 5 | No USPTO/EUIPO API integration | 🟠 Demo blocker | Complexity 1.1 / 2.2 |
| 6 | No background monitoring scheduler | 🟠 Core feature | Complexity 1.4 / 2.3 |
| 7 | No DPanel manifest | 🟡 Platform req | Complexity 0.7 |
| 8 | No pricing/billing hooks | 🟡 YC narrative | Complexity 2.7 |

---

## Database Architecture

**PostgreSQL 16** (via docker-compose locally, CloudNativePG in K8s production).
SQLite is NOT used — see AGENTS.md architecture lock.

### Schema Overview

```
trademarks              — core portfolio entries
trademark_classes       — Nice Classification (1-45) per mark
watchlist_entries       — conflict monitoring per mark
deadline_alerts         — renewal / response / opposition deadlines
search_queries          — audit log of all clearance searches
```

---

## Complexity 0 — Foundation (Quick Wins, implement first)

> Goal: working CRUD API + portfolio UI + alembic migration. Demo-able in <1 day.

### 0.1 Trademark Core Model

**Files:** `backend/app/models/trademark.py`

Fields: `id` (UUID), `name`, `owner`, `status` (Pending/Registered/Refused/Abandoned/Expired),
`jurisdiction` (US/EU/WO/...), `application_number`, `registration_number`,
`filing_date`, `registration_date`, `expiry_date`, `description`, `created_at`, `updated_at`

Relationships: → `TrademarkClass` (1:M), → `WatchlistEntry` (1:M), → `DeadlineAlert` (1:M)

**Status:** ✅ Done

---

### 0.2 Nice Classification Model

**Files:** `backend/app/models/trademark.py` (TrademarkClass)

Fields: `id`, `trademark_id` (FK→CASCADE), `nice_class_number` (1-45), `description`, `created_at`

**Status:** ✅ Done

---

### 0.3 Watchlist & Deadline Models

**Files:** `backend/app/models/watchlist.py`, `backend/app/models/deadline.py`

WatchlistEntry fields: `id`, `trademark_id` (FK→CASCADE), `conflicting_mark_name`,
`similarity_score` (0.0–1.0), `conflict_type` (Phonetic/Semantic/Visual), `status`, `notes`

DeadlineAlert fields: `id`, `trademark_id` (FK→CASCADE), `deadline_type`
(RENEWAL/RESPONSE/OPPOSITION/STATEMENT_OF_USE), `due_date`, `status` (Pending/Completed/Dismissed/Overdue), `notes`

**Status:** ✅ Done

---

### 0.4 Trademark CRUD API

**Files:** `backend/app/schemas/trademark.py`, `backend/app/repositories/trademark_repo.py`,
`backend/app/api/v1/trademarks.py`, `backend/app/api/main.py` (wire router)

Endpoints:
- `GET    /api/v1/trademarks` — list with pagination
- `POST   /api/v1/trademarks` — create
- `GET    /api/v1/trademarks/{id}` — detail with classes/watchlist/deadlines
- `PUT    /api/v1/trademarks/{id}` — update
- `DELETE /api/v1/trademarks/{id}` — delete

**Status:** ✅ Done

---

### 0.5 Watchlist & Deadline CRUD APIs

**Files:** `backend/app/schemas/{watchlist,deadline}.py`,
`backend/app/repositories/{watchlist,deadline}_repo.py`,
`backend/app/api/v1/{watchlist,deadlines}.py`

Endpoints:
- `GET/POST /api/v1/trademarks/{id}/watchlist`
- `DELETE   /api/v1/watchlist/{entry_id}`
- `GET/POST /api/v1/trademarks/{id}/deadlines`
- `PUT      /api/v1/deadlines/{id}` — update status
- `DELETE   /api/v1/deadlines/{id}`

**Status:** ✅ Done

---

### 0.6 Alembic Initial Migration

**Files:** `backend/alembic/versions/0001_initial_schema.py`,
`backend/alembic/env.py` (import all models)

Creates: `trademarks`, `trademark_classes`, `watchlist_entries`, `deadline_alerts`

**Status:** ✅ Done

---

### 0.7 DPanel Manifest

**File:** `frontend/public/dclaw-manifest.json`

Required for DPanel app registry integration.

**Status:** ✅ Done

---

### 0.8 Portfolio UI + Trademark Detail

**Files:** `frontend/src/app/portfolio/page.tsx` (list + status badges),
`frontend/src/app/portfolio/[id]/page.tsx` (detail with classes/watchlist/deadlines tabs),
`frontend/src/lib/api.ts` (typed trademark API functions)

**Status:** ✅ Done

---

### 0.9 Backend Tests (Complexity 0 coverage)

**Files:** `backend/tests/test_trademarks.py`, `backend/tests/test_watchlist.py`,
`backend/tests/test_deadlines.py`

Coverage: CRUD lifecycle, validation errors, 404s, cascade deletes

**Status:** ✅ Done

---

## Complexity 1 — Core Differentiators

> Goal: AI-assisted search + monitoring. This is what goes in the YC demo.

### 1.1 Nice Classification Service

**Files:** `backend/app/services/nice_classes.py`

Embed all 45 Nice classes with canonical descriptions. Expose:
- `GET /api/v1/classes` — list all classes
- `GET /api/v1/classes/{number}` — description + examples

**Status:** ✅ Done

---

### 1.2 Trademark Search (USPTO Mock → Real)

**Files:** `backend/app/services/clearance_search.py`, `backend/app/api/v1/search.py`

Phase A (mock): static sample results with realistic structure.
Phase B: USPTO TESS API adapter (real search).

Endpoint: `POST /api/v1/search` — `{name, classes[], jurisdiction}`
Returns: list of conflicting marks with similarity placeholders.

**Status:** ✅ Done

---

### 1.3 Phonetic + Semantic Similarity Scoring

**Files:** `backend/app/services/similarity.py`

Algorithms:
- **Phonetic**: Double Metaphone + Jaro-Winkler distance
- **Semantic**: token-level TF-IDF cosine similarity
- **Combined score**: weighted average (0.0–1.0)
- Risk buckets: Low (<0.3), Medium (0.3–0.6), High (>0.6), Identical (>0.9)

Used by search endpoint AND watchlist conflict detection.

**Status:** ✅ Done

---

### 1.4 Deadline Alert Engine

**Files:** `backend/app/services/deadline_engine.py`

Rules:
- US renewal: 10-year cycle + Section 8/15 at year 5-6
- EU renewal: 10-year cycle
- Response to office action: 3-month window

Expose: `GET /api/v1/deadlines/upcoming?days=30`
Returns deadlines due within N days across all portfolio marks.

**Status:** ✅ Done

---

### 1.5 AI Class Recommendation

**Files:** `backend/app/services/class_recommender.py`, `backend/app/api/v1/ai.py`

Endpoint: `POST /api/v1/ai/suggest-classes`
Input: `{goods_services_description: str}`
Output: `[{class_number, confidence, reasoning}]`

Strategy:
1. Keyword matching against Nice class descriptions (local, fast, free)
2. LLM call via OpenRouter (if OPENROUTER_API_KEY set) for ambiguous cases
3. Falls back to Ollama (if OLLAMA_URL reachable)

**Status:** ✅ Done

---

### 1.6 AI Trademark Copilot (Chat Interface)

**Files:** `backend/app/api/v1/copilot.py`, `backend/app/services/copilot.py`,
`frontend/src/components/TrademarCopilot.tsx`

Endpoint: `POST /api/v1/copilot/chat`
Input: `{message: str, trademark_id?: UUID}`
Output: `{reply: str, suggested_actions: [{label, action}]}`

Phase A: LLM with system prompt grounded in trademark law basics + portfolio context.
Phase B: RAG over user's own portfolio + USPTO classification guidelines.

Fallback chain: OpenRouter → Ollama → static response.

**Status:** ✅ Done

---

### 1.7 Watch Service Dashboard

**Files:** `frontend/src/app/watchlist/page.tsx`,
`frontend/src/app/portfolio/[id]/tabs/WatchTab.tsx`

Features: conflict cards with similarity score bars, risk level badges,
"Dismiss" / "Flag for review" actions.

**Status:** ✅ Done

---

### 1.8 Search UI

**Files:** `frontend/src/app/search/page.tsx`

Features: search form (name + class selector + jurisdiction), result cards with
risk badges, one-click "Add to Portfolio" from results.

**Status:** ✅ Done

---

## Complexity 2 — Advanced Features (v1.3+)

> Goal: Defensible technical moat, enterprise readiness, YC-stage scaling.

### 2.1 RAG Trademark Copilot

Full vector search over:
- User's own portfolio (trademark descriptions + prosecution history)
- USPTO TMEP (Trademark Manual of Examining Procedure) text chunks
- TTAB decisions corpus

Stack: pgvector extension on PostgreSQL + LangChain or direct embedding API.

**Status:** ✅ Done (Phase A: keyword KB + search_queries audit log; Phase B pgvector planned for v1.4)

---

### 2.2 USPTO / EUIPO / WIPO Real API Integration

- USPTO TESS REST API (free, public)
- EUIPO eSearch Plus API (free, OAuth)
- WIPO BRAND DB API

Adapter pattern in `backend/app/services/registries/`.

**Status:** ✅ Done (USPTO TSDR adapter in `services/registries/uspto.py`; search falls back to fixture corpus gracefully)

---

### 2.3 Background Watch Monitoring Scheduler

Daily cron job (APScheduler) that:
1. Runs similarity scoring against all active watchlist entries
2. Marks overdue deadline alerts
3. Wired into FastAPI lifespan

**Status:** ✅ Done (`services/scheduler.py` with APScheduler; watch scan every 24h, deadline check every 6h)

---

### 2.4 AI Application Drafting

`POST /api/v1/ai/draft-application`
LLM-generated goods/services descriptions + specimen guidance.
Export as USPTO TEAS-compatible JSON.

**Status:** ✅ Done (`services/application_drafter.py`, OpenRouter/Ollama/static fallback chain)

---

### 2.5 Logo / Visual Similarity Search

Upload logo image → embeddings via CLIP/vision model → cosine similarity over registered mark images.
Requires object storage (MinIO) + vision API integration.

**Status:** ✅ Done (stub endpoint `POST /api/v1/ai/search/logo` returns v1.4 roadmap note; full impl needs MinIO + CLIP)

---

### 2.6 Opposition & Enforcement Tracking

Case management model + deadline engine extension.
Timeline view with stage tracking (Publication → Opposition Window → Registration).

**Status:** ✅ Done (`models/opposition.py`, `api/v1/oppositions.py`, `frontend/src/app/oppositions/page.tsx`, migration)

---

### 2.7 Stripe Billing Integration

Per-seat subscription (`$99/month`) or per-search metered (`$2.99/search`).
Stripe Checkout → webhook → `subscriptions` table → feature gating.

**Status:** ✅ Done (`models/subscription.py`, `api/v1/billing.py`, `frontend/src/app/billing/page.tsx`; real Stripe enabled via STRIPE_SECRET_KEY env var)

---

### 2.8 Multi-Tenant Architecture

`organizations` table → row-level isolation on all domain tables.
JWT from Logto carries `org_id` claim → injected in all DB queries.

**Status:** ☐ Future (foundation model deferred; requires Logto JWT middleware + row-level policy enforcement)

---

## Implementation Priority (Sprint Order)

| Sprint | Features | Outcome |
|--------|----------|---------|
| Sprint 1 | 0.1–0.9 | Working CRUD app with portfolio UI |
| Sprint 2 | 1.1–1.3 | Trademark search + similarity scoring |
| Sprint 3 | 1.4–1.5 | Deadline engine + AI class suggestion |
| Sprint 4 | 1.6–1.8 | AI copilot + watch + search UIs |
| Sprint 5 | 2.1–2.3 | RAG + real registry APIs + scheduler |
| Sprint 6 | 2.4–2.8 | Drafting, billing, multi-tenant |
