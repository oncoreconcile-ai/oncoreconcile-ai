# Team Onboarding Guide

Welcome to OncoReconcile AI.

This guide helps every team member start contributing quickly.

---

## Step 1: Understand the MVP

Read:

1. `README.md`
2. `docs/mvp.md`
3. `docs/architecture.md`
4. `contracts/api_contract.md`

---

## Step 2: Pick a Task

Use GitHub Issues.

Good first tasks:

- Add benchmark cases
- Add gene aliases
- Improve API contract examples
- Build upload page
- Build reconcile endpoint
- Add explanation examples
- Write tests

---

## Step 3: Create a Branch

Use task-based branch names:

```bash
git checkout -b feature/nsclc-dataset
git checkout -b feature/reconcile-api
git checkout -b feature/upload-ui
```

Do not commit directly to `main`.

---

## Step 4: Use Vibe Coding Carefully

AI tools can help generate code, but always check:

- Does it match the API contract?
- Does it run?
- Is it small enough to review?
- Did you test it?

---

## Step 5: Submit a Pull Request

Every PR should include:

```text
What changed?
How did you test it?
Screenshot or sample output if applicable.
What issue does it close?
```

---

## Step 6: Ask for Help Early

If blocked for more than 48 hours, post:

```text
Blocked by:
What I tried:
What I need:
```

---

## Team Rule

Do not wait for Justin to make every decision.

If the decision is small, make it, document it in `docs/decisions.md`, and keep moving.
