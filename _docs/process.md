# Delivery process

References: https://aishippingblog.com/p/ai-native-development-specifications and https://aishippingblog.com/p/build-and-ship-a-full-stack-app-with . Combine specification/role separation with frontend-first incremental execution.

1. PM defines scope, architecture, acceptance criteria, dependencies and existing GitHub Issues before feature implementation.
2. Engineer reads one or a coherent group of issues, implements within the current iteration, adds meaningful tests, runs checks and commits with issue references.
3. Engineer sends changed files, commands/results, limitations and commit to independent QA.
4. QA independently checks acceptance criteria and actual workflows. Record PASS/FAIL and reproducible evidence. Only verified PASS can close an MVP issue.
5. Real failure becomes a `user-test-bug` issue with steps, expected/actual behavior and environment. PM grooms acceptance criteria; QA specifies regression; engineer fixes; QA reruns and closes after PASS.
6. Leave `post-mvp` issues open. Never create fake defects or fabricate approvals, historical conversations, screenshots, timestamps or CI results.

Use the iterative order in `_docs/plan.md`. Keep the mock service available after integration for demonstration and tests. All tests must isolate their databases. The final audit checks required files, persistence, browser workflow, build, contract, real GitHub Actions status and closed MVP/bug issues.
