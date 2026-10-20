# Chat Brainstorm — SplitWise Pro

> **Provenance:** This document separates real user messages available in the conversation record from summarized decisions and AI/PM analysis. The analysis sections are **not** fabricated chat messages or verbatim historical transcripts. A complete original chat export was not available to reconstruct.

## 1. University assignment: what must be built

The user provided a Part II AI-native development assignment requiring:

- Follow the AI-native specifications and full-stack iteration articles.
- Use real GitHub Issues with `mvp`, `post-mvp` and `user-test-bug` labels.
- Define agent roles, PM grooming, independent QA and meaningful acceptance criteria.
- Create frontend using `mockService` first; next write `openapi.yml`; then an in-memory backend; then SQLite through a DBMS-agnostic ORM; finally connect and test the integrated app.
- Use strong design references or a non-generic design agent.
- Preserve Markdown documents and genuine brainstorming history.
- Execute real tests, file bugs found through testing, and close verified MVP/bug issues before the deadline.

References:
1. https://aishippingblog.com/p/ai-native-development-specifications
2. https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with

## 2. Actual available user conversation excerpts

These excerpts are user-authored messages available to the project planning context; their order is preserved where known. They are **not** a reconstructed assistant/user dialogue.

**User — app choice (original):**
> SplitWise Pro — Shared Expense Manager

**User — request to implement according to the professor (original):**
> я выбрал этого и ты мне дай промпт который все сделает ии проект должен быть как сказано преподаватель

**User — time constraint (original):**
> дедлайн через 10 часов

**User — GitHub repository (original URL):**
> https://github.com/Usmanovkairat/splitwise-pro

**User — continuation (original):**
> дальше продолжай

**User — request to simplify (original):**
> сделай этот проект более легким путем

**User — request for autonomous completion (original):**
> нет ты сам не можешь сделать весь проект?

**User — authorization to continue modifying the existing repository (original):**
> да

**User — request to check the professor's requirements (original):**
> проект содержит эти категории?

**User — request to clarify code and improve this file (original):**
> там коды, backend, frontend и тд нету коды добавь их и сделай chat-brainstorm.md еще раз более четко

Some of these messages occurred after the original planning stage. They are included for transparent provenance, **not** presented as pre-implementation brainstorming.

## 3. Ideas considered — PM analysis, not invented user dialogue

| Candidate | Main value | Why not selected as a separate app |
| --- | --- | --- |
| Roommate expense ledger | Split rent, utilities and groceries | Too narrow if limited to recurring household bills |
| Travel expense splitter | Track shared costs with different participants | Useful, but should also support everyday groups |
| Reimbursement approval dashboard | Employee expense approvals | Introduces unnecessary company roles and authorization |
| **SplitWise Pro** | Groups, precise splitting, balances and repayments | **Chosen:** useful real-world workflow with a testable domain model |

**Decision rationale:** Combine household and travel use cases in one small group-expense workspace. Avoid implementing banking or real money transfers.

## 4. Product definition

**Problem:** Friends, roommates and travel groups often struggle to remember who paid, how shared bills should be divided, and how much remains owed after partial repayments.

**Target users:** Small groups managing informal shared expenses on one local computer.

**MVP user journey:**
1. Create a group (e.g. an Almaty weekend trip).
2. Add several members.
3. Add a bill and choose the payer and participants.
4. Split equally, by exact amounts, or by percentages.
5. Review per-member net balances and suggested repayments.
6. Record a partial settlement.
7. Refresh the page or restart the backend and confirm the data remains.

**Out of scope for MVP:** Authentication, real payments, cloud hosting, multi-tenant access, currency conversion and CSV export.

## 5. Technical decisions and reasons — AI/PM planning record

| Decision | Reason |
| --- | --- |
| React + TypeScript + Vite | Component-based responsive frontend with typed service contracts |
| `mockService` first | Build and test UI independently before a backend exists |
| `openapi.yml` as source contract | Keep frontend/backend expectations explicit and verifiable |
| FastAPI in-memory implementation | Validate API semantics before persistence complexity |
| SQLAlchemy 2 + Alembic + SQLite | Persistent relational data with ORM and reproducible migrations |
| Integer minor currency units | Avoid floating-point accounting errors |
| Stable deterministic rounding | Every allocation must sum exactly to the original expense |
| Partial settlement constraints | Prevent recording repayment greater than outstanding debt |
| pytest, Vitest, Playwright | Cover domain invariants, services and real browser workflows |

**Design reference choice:** Linear (navigation and information hierarchy), Ramp (spending cards) and Mercury (restrained financial typography). This is a documented alternative permitted by the assignment; **no claim of a Lovable/v0/Claude Design session is made**. Details: `_docs/design-system.md`.

## 6. AI-native iteration history and evidence

The repository preserves distinct implementation commits. This is a summary of documented work, not a fabricated chat transcript.

| Stage | Deliverable | Evidence |
| --- | --- | --- |
| Planning | Scope, agent roles, GitHub issue backlog | `_docs/plan.md`, `AGENTS.md`, `_docs/qa/planning.md` |
| Frontend-first | Real pages and deterministic `mockService` | `frontend/src/`, `_docs/qa/mock-frontend.md` |
| API contract | OpenAPI source document and validation | `openapi.yml`, `_docs/qa/contract.md` |
| In-memory backend | FastAPI routes without database | `backend/app/`, `_docs/qa/memory-backend.md` |
| Persistent backend | SQLite, SQLAlchemy ORM and Alembic | `backend/app/models.py`, `backend/migrations/`, `_docs/qa/sqlite.md` |
| Integration | Typed HTTP service and actual browser workflows | `frontend/src/services/`, `_docs/qa/integration.md` |
| Independent QA | Automated tests, real bug reports and fixes | `_docs/qa/final.md`, GitHub Issues #34–#41 |

For actual commit IDs and order, see `_docs/iterations.md`. Do not infer that all steps occurred in one chat session.

## 7. Real bugs and how the process responded

The QA reports document actual observed defects and retests, including:
- #34: horizontal overflow on a 390 px screen.
- #35: unsuccessful mutation displayed misleading feedback.
- #36: saved display name did not update the sidebar.
- #37: duplicate member names handled differently by mock and backend.
- #38: group rename sent an immutable currency field.
- #39: direct group URLs opened the wrong group.
- #40: dialog close did not return keyboard focus.
- #41: insufficient contrast for small text.

Issues contain goal/description/acceptance criteria; PM/engineer/QA handoffs and tests are recorded in repository QA files. These are not fictional example bugs.

## 8. Final scope and how to demonstrate it

Run the project using `README.md`. Show a group, members, multiple split methods, balances, partial repayment and persistence after refresh. Show `openapi.yml`, SQLite/ORM models, the commit history, GitHub Issues, agent role Markdown files and the real QA evidence.

The actual executed test counts and hosted CI link are in `SUBMISSION.md` and `_docs/qa/final.md`. The app is a local-first workspace, not a deployed multi-user payment service.

## 9. Integrity note

This is a **clearer, edited record of the brainstorming and decision trail**. Only quoted user messages are represented as direct user speech. Candidate comparisons, design rationale and technical decisions are explicitly attributed to PM/AI analysis. No missing assistant messages, tool runs, user interviews or pre-implementation conversations have been invented.
