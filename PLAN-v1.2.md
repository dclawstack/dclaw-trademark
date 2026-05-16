# DClaw Trademark — v1.2 Feature Roadmap

> 📘 **REVISED PRD v2.3 available:** See `REVISED-PRD.md` for complete gap analysis, current state, and full feature roadmap.


> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (tm-search-tools), AI product research (Corsearch, TrademarkNow, Anaqua, Clarivate)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Trademark portfolio CRUD
- [ ] Search & watch services
- [ ] Filing deadline tracking
- [ ] Document management
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Trademark Copilot (Clearance Assistant)
**Description:** AI assistant that evaluates trademark strength, suggests classes, checks similarity, and flags risks. "Can I register 'Nexora' for software?"
- **AI Angle:** RAG over trademark databases + classification guidelines. LLM risk assessment.
- **Backend:** `/api/v1/ai/trademark-check` endpoint.
- **Frontend:** Chat interface with clearance report cards.
- **Files:** `backend/app/services/tm_ai.py`, `frontend/src/components/tm-copilot.tsx`

#### 2. Trademark Clearance Search
**Description:** Search USPTO TESS, EUIPO, WIPO databases. AI ranks similar marks by likelihood of confusion.
- **Backend:** Trademark API integration. Similarity scoring (phonetic + semantic).
- **Frontend:** Search results with confusion risk badges.
- **Files:** `backend/app/services/clearance_search.py`

#### 3. Portfolio Management & Docketing
**Description:** Track trademark applications, registrations, renewals, and oppositions. Deadline alerts.
- **Backend:** Docketing engine with country-specific rules.
- **Frontend:** Portfolio grid with status indicators. Deadline calendar.
- **Files:** `backend/app/services/tm_docketing.py`

#### 4. Watch & Monitoring Service
**Description:** Monitor new trademark filings that may conflict with your portfolio. Alert on potential infringements.
- **Backend:** Watch list matching engine. Daily monitoring job.
- **Frontend:** Watch list manager. Alert feed.
- **Files:** `backend/app/services/watch_service.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Class Recommendation
**Description:** AI suggests Nice Classification classes based on goods/services description.
- **AI Angle:** LLM classification with trademark office guidelines.
- **Backend:** `/api/v1/ai/suggest-classes` endpoint.
- **Frontend:** Class suggestion panel in filing form.

#### 6. Filing Workflow & Forms
**Description:** Guided trademark filing workflow. Auto-populate forms. E-filing integration (TEAS/EM).
- **Backend:** Form generation engine. E-filing API adapters.
- **Frontend:** Step-by-step filing wizard. Form preview.

#### 7. Opposition & Dispute Tracking
**Description:** Track oppositions, cancellations, and disputes. Deadline management.
- **Backend:** Dispute case management.
- **Frontend:** Dispute board with stage tracking.

#### 8. Brand Guidelines & Usage Tracker
**Description**: Store brand guidelines. Track licensed usage. Monitor unauthorized use.
- **Backend:** Guideline document storage. Usage tracking.
- **Frontend:** Brand portal. Usage analytics.

### P2 — Could Have (v1.3+)

#### 9. Logo Similarity Search (Vision AI)
**Description:** Upload a logo image. Find visually similar registered marks.

#### 10. Domain & Social Handle Availability
**Description:** Check domain and social media handle availability alongside trademark clearance.

#### 11. AI-Generated Trademark Descriptions
**Description:** Auto-write goods/services descriptions optimized for approval.

#### 12. Global Portfolio Cost Optimizer
**Description:** AI recommends filing strategies (Madrid vs national) to minimize costs.

---

## Implementation Priority

1. **Week 1–2:** AI Trademark Copilot (P0.1) + Clearance Search (P0.2)
2. **Week 3–4:** Portfolio Docketing (P0.3) + Watch Service (P0.4)
3. **Week 5–6:** Class Recommendation (P1.5) + Filing Workflow (P1.6)
4. **Week 7–8:** Opposition Tracking (P1.7) + Brand Guidelines (P1.8)
