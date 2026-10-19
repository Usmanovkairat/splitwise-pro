# Architecture and decisions

React/TypeScript/Vite owns navigation, forms and presentation. A typed service boundary has deterministic mockService and HTTP adapters. TanStack Query owns asynchronous cache/invalidation. Tailwind/shadcn-style primitives, Lucide and Recharts provide accessible reusable UI and analytics.

FastAPI/Pydantic validates transport data. Domain functions calculate integer expense shares, balances and settlement suggestions independently of HTTP/storage. Repository implementations share behavior: iteration 3 is memory-only; iteration 4 adds SQLAlchemy 2 and SQLite behind the same interface. Alembic owns schema evolution; configuration chooses storage and a configurable database URL preserves ORM portability.

Resources: Group → Members, Expenses and Settlements; Expense → Shares. IDs are strings. Group has one of KZT/USD/EUR/GBP. Referenced members cannot be removed. Deleting a group is an explicit confirmed cascade. Expense/share writes and settlement validation/write run atomically; isolated test databases prevent cross-test contamination. SQLite foreign keys are enabled.

## Money rules
All stored/API money uses integer minor units. Equal split uses unit weights. Exact split directly validates integer allocations summing to the total. Percentage split uses integer basis points totaling 10000. Weighted allocation floors each quotient, then distributes remaining units by descending remainder, ties ascending member ID. Sum(shares) equals expense amount.

Member net = paid − owed + sent settlements − received settlements. Positive net is receivable; negative net is debt. Group net always sums to zero. Settlement suggestions pair sorted current debtors/creditors deterministically and reduce remaining amounts. A recorded settlement must be positive, connect distinct group members from negative to positive net, and stay within both outstanding amounts. It records repayment; it does not transfer funds.

## API contract
`openapi.yml` is the reviewed source contract, created after mock frontend and before backend. `/api/groups/{id}/members`, `/expenses`, `/settlements`, `/balances`, and `/analytics` preserve group context. Standard not-found, validation and conflict responses allow consistent UI feedback. Filtering/pagination must be documented where implemented. Runtime/schema alignment is verified rather than assumed.

## Decisions and exclusions
Keep one local workspace with no authentication, cloud dependency, exchange rates or payment processing. Never add unlike currencies into one monetary figure. Keep mock mode after integration for deterministic UI tests. Store only source and migrations in Git; local database files are ignored. CSV statements and multi-workspace authentication are tracked separately as post-MVP.
