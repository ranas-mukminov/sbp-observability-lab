"""AI provider abstractions."""
from __future__ import annotations

from typing import Iterable, List

from sbp_observability.models import ErrorClass


class AIProvider:
    def classify_errors(self, errors: Iterable[str]) -> List[ErrorClass]:
        raise NotImplementedError

    def generate_report(self, summary: str) -> str:
        raise NotImplementedError


class NoopAIProvider(AIProvider):
    """Deterministic provider for tests."""

    def classify_errors(self, errors: Iterable[str]) -> List[ErrorClass]:
        result: List[ErrorClass] = []
        for error in errors:
            if "timeout" in error.lower():
                result.append(
                    ErrorClass(
                        name="GATEWAY_TIMEOUT",
                        pattern="timeout",
                        severity="warn",
                        description_ru="Таймаут при обращении к банку",
                    )
                )
            elif "decline" in error.lower():
                result.append(
                    ErrorClass(
                        name="BANK_DECLINE",
                        pattern="decline",
                        severity="critical",
                        description_ru="Отказ банка-участника",
                    )
                )
            else:
                result.append(
                    ErrorClass(
                        name="UNKNOWN",
                        pattern=error,
                        severity="info",
                        description_ru="Неизвестная ошибка",
                    )
                )
        return result

    def generate_report(self, summary: str) -> str:
        return f"Отчёт по СБП:\n{summary}\n"
