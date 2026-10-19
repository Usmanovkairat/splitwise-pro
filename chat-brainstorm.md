# Brainstorming record and product decisions

## Genuine available conversation
The available earlier conversation contains the user's selection: “SplitWise Pro — Shared Expense Manager” and “я выбрал этого и ты мне дай промпт который все сделает ии проект должен быть как сказано преподаватель” (I chose this; give me a prompt that makes the AI do everything according to the professor).

In this session the user attached the master assignment and said “дедлайн через 10 часов” (deadline in ten hours). The assistant asked the user to create an empty public repository because the available connector could not create it. The user supplied https://github.com/Usmanovkairat/splitwise-pro . These are the conversation facts available; no unseen brainstorming transcript is reconstructed as dialogue.

## PM brainstorming performed during planning
This section is current PM analysis, not invented user speech. Considered directions: a roommate bill ledger emphasizes recurring household costs; a trip expense splitter emphasizes varying participation and unequal shares; a lightweight reimbursement dashboard emphasizes company approval flows. The selected SplitWise Pro combines the first two: group records, three allocation methods, deterministic debt simplification and analytics. Corporate approvals, real payments and authentication would dilute the local-first demonstration and are excluded.

Why it differs from Part I: StudyFlow is a Flask student task tracker. This project is a React/FastAPI financial-recording application with precise integer allocation, relational accounting history, debt suggestions, settlement constraints and charts. StudyFlow remains untouched.

Decision: build a single-workspace MVP for friends, roommates and travelers. Demonstration story: create a trip, add three friends, divide an uneven bill, add a percentage expense, inspect net balances, record a partial repayment and refresh/restart to verify persistence. Success means this story works in the real browser and all invariants and issue criteria pass independent QA.

Technical choices follow the attached assignment: frontend-first mockService, OpenAPI source contract, in-memory API, then SQLAlchemy/Alembic SQLite and typed HTTP integration in distinct commits. Detailed scope and numerical rules are in `_docs/plan.md`. No claim is made that the user personally proposed each implementation detail.
