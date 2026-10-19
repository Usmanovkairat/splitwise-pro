# AI-native development agreement

SplitWise Pro is a local-first shared expense workspace, separate from StudyFlow (a Flask student task tracker). Follow `_docs/plan.md`, `_docs/process.md`, the OpenAPI contract and the issue acceptance criteria.

The orchestrator coordinates an actual PM agent, frontend engineer, backend engineer and independent QA agent. Engineers implement and execute checks; they cannot declare their own QA PASS. QA independently reviews evidence, runs acceptance checks and closes an issue only after PASS. PM grooms real reported bugs; do not manufacture bugs to demonstrate workflow.

Required chronological stages: planning; frontend with mockService; OpenAPI; in-memory backend; SQLite/SQLAlchemy; integration; browser QA and fixes; final verification. Commit stages separately, reference existing real issue numbers, and never rewrite history to simulate earlier work.

Money is integer minor units. Each group has one currency from KZT/USD/EUR/GBP, all with two decimals. Equal/percentage rounding uses largest remainder, ties ascending stable member ID. Percentages use basis points totaling 10000. No authentication, money transfer or banking integration. Never expose credentials, commit user databases, invent chat or report unexecuted tests.
