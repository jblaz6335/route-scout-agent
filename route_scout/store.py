from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Protocol

from .models import Opportunity, Recommendation, RecordedDecision


class DecisionStore(Protocol):
    def save(self, opportunity: Opportunity, recommendation: Recommendation) -> str: ...

    def list_recent(self, limit: int = 20) -> list[dict]: ...


class MemoryDecisionStore:
    def __init__(self) -> None:
        self._items: list[dict] = []

    def save(self, opportunity: Opportunity, recommendation: Recommendation) -> str:
        record = RecordedDecision(
            opportunity=opportunity,
            recommendation=recommendation,
            recorded_at=datetime.now(UTC).isoformat(),
        ).model_dump(mode="json")
        record_id = f"route-{len(self._items) + 1:04d}"
        record["id"] = record_id
        self._items.insert(0, record)
        return record_id

    def list_recent(self, limit: int = 20) -> list[dict]:
        return self._items[:limit]


class FirestoreDecisionStore:
    def __init__(self) -> None:
        from google.cloud import firestore

        self._collection = firestore.Client().collection("route_scout_decisions")

    def save(self, opportunity: Opportunity, recommendation: Recommendation) -> str:
        record = RecordedDecision(
            opportunity=opportunity,
            recommendation=recommendation,
            recorded_at=datetime.now(UTC).isoformat(),
        ).model_dump(mode="json")
        document = self._collection.document()
        document.set(record)
        return document.id

    def list_recent(self, limit: int = 20) -> list[dict]:
        query = self._collection.order_by("recorded_at", direction="DESCENDING").limit(limit)
        return [{"id": item.id, **item.to_dict()} for item in query.stream()]


def create_store() -> DecisionStore:
    if os.getenv("ROUTE_SCOUT_STORE", "memory").lower() == "firestore":
        return FirestoreDecisionStore()
    return MemoryDecisionStore()
