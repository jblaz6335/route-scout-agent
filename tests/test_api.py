from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_names_required_stack() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model"] == "gemini-3.5-flash"
    assert "Google ADK" in response.json()["agent_framework"]


def test_score_records_a_decision() -> None:
    response = client.post(
        "/api/score",
        json={
            "title": "Automation bounty",
            "summary": "Build a tested Python API automation workflow for a public contest.",
            "requirements": ["Python", "API", "automation", "testing"],
            "prize_usd": 2500,
            "days_remaining": 12,
        },
    )
    assert response.status_code == 200
    assert response.json()["id"].startswith("route-")
    assert client.get("/api/decisions").json()


def test_demo_has_three_distinct_routes_to_compare() -> None:
    response = client.get("/api/demo")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 3
    assert len({item["recommendation"]["route"] for item in payload}) >= 2


def test_agent_endpoint_rejects_vague_prompts_before_model_call() -> None:
    response = client.post("/api/agent", json={"prompt": "too short"})
    assert response.status_code == 422
