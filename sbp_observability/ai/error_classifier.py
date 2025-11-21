"""Error classification logic."""
from __future__ import annotations

from typing import Iterable, List

from sbp_observability.ai.ai_provider import AIProvider, NoopAIProvider
from sbp_observability.models import ErrorClass

BASE_RULES = {
    "timeout": ErrorClass(
        name="GATEWAY_TIMEOUT",
        pattern="timeout",
        severity="warn",
        description_ru="Таймаут при обращении к шлюзу",
    ),
    "decline": ErrorClass(
        name="BANK_DECLINE",
        pattern="decline",
        severity="critical",
        description_ru="Отказ банка",
    ),
}


def classify(errors: Iterable[str], provider: AIProvider | None = None) -> List[ErrorClass]:
    provider = provider or NoopAIProvider()
    results: List[ErrorClass] = []
    for error in errors:
        normalized = error.lower()
        matched = next((rule for key, rule in BASE_RULES.items() if key in normalized), None)
        if matched:
            results.append(matched)
        else:
            results.extend(provider.classify_errors([error]))
    return results
