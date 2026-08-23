from route_scout.models import Opportunity, Route
from route_scout.scoring import score_opportunity


def test_strong_fit_routes_to_build_now() -> None:
    result = score_opportunity(
        Opportunity(
            title="Python AI automation agent",
            summary=(
                "Build a Python workflow agent with Google Cloud, FastAPI, automated testing, "
                "and a public API."
            ),
            requirements=["Python", "AI agents", "Google Cloud", "testing"],
            prize_usd=40_000,
            days_remaining=14,
        )
    )
    assert result.route is Route.BUILD_NOW
    assert result.score >= 68
    assert "python" in result.matched_skills
    assert result.evidence


def test_paid_reputation_gate_lowers_route() -> None:
    result = score_opportunity(
        Opportunity(
            title="Members-only design contract",
            summary="A paid marketplace contract requiring a long design reputation history.",
            requirements=["UI design"],
            prize_usd=500,
            days_remaining=10,
            requires_payment=True,
            requires_existing_reputation=True,
        )
    )
    assert result.route is Route.SKIP
    assert result.breakdown.penalties == 30


def test_unknown_identity_is_a_hard_penalty() -> None:
    result = score_opportunity(
        Opportunity(
            title="Cloud automation challenge",
            summary="Build a Python automation workflow with an unavailable verified identity.",
            requirements=["Python", "automation", "workflow"],
            prize_usd=1_000,
            days_remaining=20,
            requires_unavailable_identity=True,
        )
    )
    assert result.breakdown.penalties == 30
    assert result.route in {Route.VERIFY_FIRST, Route.SKIP}


def test_zero_value_route_still_gets_economics_floor() -> None:
    result = score_opportunity(
        Opportunity(
            title="Open source Python task",
            summary="A volunteer Python maintenance task with tests and no cash bounty.",
            requirements=["Python", "testing"],
            prize_usd=0,
            days_remaining=60,
        )
    )
    assert result.breakdown.economics == 2
