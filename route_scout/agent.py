from __future__ import annotations

import json

from google.adk.agents import Agent

from .models import Opportunity
from .profile import EVIDENCE, SKILLS
from .scoring import score_opportunity


def get_operator_profile() -> dict:
    """Return the operator's capability inventory and public proof links."""
    return {
        "skills": sorted(SKILLS),
        "evidence": [item.model_dump(mode="json") for item in EVIDENCE],
    }


def evaluate_route(
    title: str,
    summary: str,
    requirements_json: str = "[]",
    prize_usd: int = 0,
    days_remaining: int = 30,
    requires_payment: bool = False,
    requires_existing_reputation: bool = False,
    requires_unavailable_identity: bool = False,
) -> dict:
    """Score one opportunity against verified skills, evidence, timing, and friction."""
    requirements = json.loads(requirements_json)
    opportunity = Opportunity(
        title=title,
        summary=summary,
        requirements=requirements,
        prize_usd=prize_usd,
        days_remaining=days_remaining,
        requires_payment=requires_payment,
        requires_existing_reputation=requires_existing_reputation,
        requires_unavailable_identity=requires_unavailable_identity,
    )
    return score_opportunity(opportunity).model_dump(mode="json")


root_agent = Agent(
    name="route_scout",
    model="gemini-3.5-flash",
    description=(
        "Turns noisy bounties, hackathons, and contract listings into evidence-backed "
        "build-now, verify-first, or skip routes."
    ),
    instruction=(
        "You are Route Scout, an execution-focused opportunity analyst for a solo developer. "
        "Never invent eligibility, revenue, account access, or proof. First call "
        "get_operator_profile. Then extract concrete requirements from the opportunity and call "
        "evaluate_route. Explain the score, cite matching public evidence returned by the tool, "
        "and end with no more than three next actions. Treat payment, identity, and platform "
        "reputation requirements as explicit gates. Do not apply, register, spend, or message "
        "anyone."
    ),
    tools=[get_operator_profile, evaluate_route],
)
