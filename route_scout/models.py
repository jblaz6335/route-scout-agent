from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Route(StrEnum):
    BUILD_NOW = "build_now"
    VERIFY_FIRST = "verify_first"
    SKIP = "skip"


class Opportunity(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    source_url: HttpUrl | None = None
    summary: str = Field(min_length=20, max_length=5000)
    requirements: list[str] = Field(default_factory=list, max_length=30)
    prize_usd: int = Field(default=0, ge=0, le=10_000_000)
    days_remaining: int = Field(default=30, ge=0, le=3650)
    requires_payment: bool = False
    requires_existing_reputation: bool = False
    requires_unavailable_identity: bool = False

    @field_validator("requirements")
    @classmethod
    def normalize_requirements(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item.strip()]


class Evidence(BaseModel):
    label: str
    url: HttpUrl
    skills: list[str]
    proof: str


class ScoreBreakdown(BaseModel):
    fit: int = Field(ge=0, le=55)
    economics: int = Field(ge=0, le=25)
    urgency: int = Field(ge=0, le=10)
    evidence: int = Field(ge=0, le=10)
    penalties: int = Field(ge=0, le=100)


class Recommendation(BaseModel):
    route: Route
    score: int = Field(ge=0, le=100)
    breakdown: ScoreBreakdown
    matched_skills: list[str]
    evidence: list[Evidence]
    reasons: list[str]
    next_actions: list[str]


class RecordedDecision(BaseModel):
    opportunity: Opportunity
    recommendation: Recommendation
    recorded_at: str
