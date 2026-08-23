from __future__ import annotations

from .models import Evidence

SKILLS = {
    "python",
    "api",
    "automation",
    "ai agents",
    "google cloud",
    "fastapi",
    "firestore",
    "github actions",
    "javascript",
    "sqlite",
    "testing",
    "workflow",
}

EVIDENCE = [
    Evidence(
        label="Decision Gate",
        url="https://devpost.com/software/decision-gate",
        skills=["python", "ai agents", "workflow", "sqlite", "testing"],
        proof="Submitted Strands agent with a live demo, public source, and green CI.",
    ),
    Evidence(
        label="Packet Proof",
        url="https://devpost.com/software/packet-proof",
        skills=["python", "api", "automation", "testing"],
        proof="Submitted verification workflow with 80 tests and branch-aware coverage.",
    ),
    Evidence(
        label="Blaz Algo Systems",
        url="https://blazalgosystems.netlify.app/proof-of-work/",
        skills=["automation", "api", "fastapi", "javascript", "workflow"],
        proof="Public proof hub with scoped services, tested kits, and live artifacts.",
    ),
]
