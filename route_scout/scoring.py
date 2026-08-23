from __future__ import annotations

import math
import re

from .models import Opportunity, Recommendation, Route, ScoreBreakdown
from .profile import EVIDENCE, SKILLS

TOKEN_RE = re.compile(r"[a-z0-9+#.]+")


def _tokens(value: str) -> set[str]:
    return set(TOKEN_RE.findall(value.lower()))


def _matched_skills(opportunity: Opportunity) -> list[str]:
    haystack = " ".join([opportunity.title, opportunity.summary, *opportunity.requirements]).lower()
    return sorted(skill for skill in SKILLS if skill in haystack)


def score_opportunity(opportunity: Opportunity) -> Recommendation:
    matched = _matched_skills(opportunity)
    fit = min(55, len(matched) * 9)

    if opportunity.prize_usd <= 0:
        economics = 2
    else:
        economics = min(25, 5 + round(5 * math.log10(opportunity.prize_usd)))

    if opportunity.days_remaining <= 1:
        urgency = 2
    elif opportunity.days_remaining <= 10:
        urgency = 10
    elif opportunity.days_remaining <= 30:
        urgency = 8
    else:
        urgency = 4

    matching_evidence = [item for item in EVIDENCE if set(item.skills).intersection(matched)]
    evidence_score = min(10, len(matching_evidence) * 4)

    penalties = 0
    reasons: list[str] = []
    if opportunity.requires_payment:
        penalties += 18
        reasons.append("Entry requires payment or a financial commitment.")
    if opportunity.requires_existing_reputation:
        penalties += 12
        reasons.append("The route depends on reputation that is not yet proven on-platform.")
    if opportunity.requires_unavailable_identity:
        penalties += 30
        reasons.append("A required identity or account is not currently available.")

    score = max(0, min(100, fit + economics + urgency + evidence_score - penalties))
    if score >= 68:
        route = Route.BUILD_NOW
    elif score >= 42:
        route = Route.VERIFY_FIRST
    else:
        route = Route.SKIP

    if matched:
        reasons.insert(0, f"Matched capabilities: {', '.join(matched)}.")
    else:
        reasons.insert(0, "No direct capability match was found in the current proof inventory.")
    reasons.append(f"Prize or contract value contributes {economics} of 25 economics points.")
    reasons.append(f"Deadline contributes {urgency} of 10 urgency points.")

    next_actions = {
        Route.BUILD_NOW: [
            "Verify official rules and required submission fields.",
            "Create a dated execution plan tied to existing public evidence.",
            "Build the smallest working judgeable artifact first.",
        ],
        Route.VERIFY_FIRST: [
            "Resolve the missing eligibility, payment, or account requirement.",
            "Estimate build hours before committing the route.",
            "Promote to build_now only when the gate is cleared.",
        ],
        Route.SKIP: [
            "Archive the route with its rejection reason.",
            "Move capacity to a higher-scoring opportunity.",
        ],
    }[route]

    return Recommendation(
        route=route,
        score=score,
        breakdown=ScoreBreakdown(
            fit=fit,
            economics=economics,
            urgency=urgency,
            evidence=evidence_score,
            penalties=penalties,
        ),
        matched_skills=matched,
        evidence=matching_evidence,
        reasons=reasons,
        next_actions=next_actions,
    )
