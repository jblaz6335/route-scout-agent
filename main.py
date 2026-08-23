from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from google.adk.runners import InMemoryRunner
from pydantic import BaseModel, Field

from route_scout.agent import root_agent
from route_scout.models import Opportunity
from route_scout.scoring import score_opportunity
from route_scout.store import create_store

BASE_DIR = Path(__file__).parent
app = FastAPI(title="Route Scout", version="0.1.0")
store = create_store()
runner = InMemoryRunner(agent=root_agent, app_name="route_scout")


class AgentRequest(BaseModel):
    prompt: str = Field(min_length=20, max_length=8_000)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "agent_framework": "Google ADK 2.7.1",
        "model": "gemini-3.5-flash",
        "store": type(store).__name__,
    }


@app.post("/api/score")
def score(payload: Opportunity) -> dict:
    recommendation = score_opportunity(payload)
    record_id = store.save(payload, recommendation)
    return {"id": record_id, **recommendation.model_dump(mode="json")}


@app.get("/api/decisions")
def decisions() -> list[dict]:
    return store.list_recent()


@app.post("/api/agent")
async def ask_agent(payload: AgentRequest) -> dict:
    """Run the Google ADK agent and return its final evidence-backed explanation."""
    try:
        events = await runner.run_debug(
            payload.prompt,
            user_id="route-scout-web",
            session_id=f"web-{uuid4().hex}",
            quiet=True,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Gemini is unavailable. Verify the Vertex AI project and runtime identity.",
        ) from exc

    for event in reversed(events):
        if not event.is_final_response() or not event.content:
            continue
        text = "".join(part.text or "" for part in event.content.parts if part.text)
        if text:
            return {"response": text, "event_count": len(events)}
    raise HTTPException(status_code=502, detail="The agent completed without a text response.")


@app.get("/api/demo")
def demo() -> list[dict]:
    fixtures = [
        Opportunity(
            title="Agents for Humans Hackathon",
            summary=(
                "Build a professional AI agent with Python and Strands Agents SDK. "
                "Public repository, tests, live demo, and architecture are required."
            ),
            requirements=["Python", "AI agents", "workflow", "testing"],
            prize_usd=40_000,
            days_remaining=23,
        ),
        Opportunity(
            title="All Things Agentic",
            summary=(
                "Build an asynchronous Google ADK agent with Gemini 3.5 and deploy it "
                "to Google Cloud with a public demonstration."
            ),
            requirements=["Google Cloud", "AI agents", "Python", "workflow"],
            prize_usd=180_000,
            days_remaining=9,
        ),
        Opportunity(
            title="Paid membership design marketplace",
            summary=(
                "Applicants must pay a monthly membership and show five years of UI design "
                "reputation before they can submit proposals."
            ),
            requirements=["UI design", "existing platform reputation"],
            prize_usd=500,
            days_remaining=14,
            requires_payment=True,
            requires_existing_reputation=True,
        ),
    ]
    return [
        {
            "opportunity": item.model_dump(mode="json"),
            "recommendation": score_opportunity(item).model_dump(mode="json"),
        }
        for item in fixtures
    ]
