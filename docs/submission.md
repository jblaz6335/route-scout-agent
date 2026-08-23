# Route Scout submission draft

## One-line pitch

Route Scout is a Google ADK agent that turns noisy hackathons, bounties, and
contract listings into an evidence-backed decision: build now, verify first, or
skip.

## Inspiration

Opportunity discovery is cheap. A solo developer's scarce resource is focused
execution time. Lists grow faster than projects ship, requirements stay buried in
long pages, and attractive prize numbers can hide payment gates, reputation gates,
or impossible deadlines. Route Scout was built to make the commitment decision
auditable before another build starts.

## What it does

The agent extracts concrete skills, economics, timing, and blockers from an
opportunity. It reads a verified capability profile, calls a deterministic scoring
tool, ties matches to public proof, and routes the opportunity to `build_now`,
`verify_first`, or `skip`. The web app also keeps a Firestore-ready ledger so the
operator can review past decisions instead of circling the same routes.

## How it was built

- Google ADK 2.7.1 defines the agent and its bounded tools.
- Gemini 3.5 Flash extracts and explains the route.
- FastAPI exposes the product UI, scorer, and live ADK runner.
- Cloud Run hosts the containerized service.
- Firestore stores production decisions; tests use an in-memory adapter.
- A deterministic scorer makes the economic and blocker logic testable.

## Responsible-agent boundary

Route Scout records decisions, not applications. Its tools cannot register, bid,
spend, submit, send messages, or claim revenue. Public proof is cited when present,
and missing eligibility or identity information becomes a visible gate rather than
an invented fact.

## Accomplishments

- Eight automated API and scoring tests with 89% measured package coverage.
- A working responsive decision surface and live Google ADK endpoint.
- An auditable scoring policy that separates capability fit, economics, urgency,
  evidence, and blockers.
- A new project created entirely during the competition period.

## Links

- Source: https://github.com/jblaz6335/route-scout-agent
- Architecture: https://github.com/jblaz6335/route-scout-agent/blob/main/docs/architecture.svg
- Live demo: pending Cloud Run deployment

## Four-minute demo outline

1. Show the growing opportunity problem and the three route outcomes.
2. Run the verified three-opportunity demo set.
3. Score a concrete Python automation contract.
4. Ask Gemini to explain the decision and show the ADK tool trace.
5. Open the architecture diagram and Firestore-backed decision ledger.
6. Close on the safety boundary and why evidence beats opportunity volume.
