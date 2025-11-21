"""Generate human readable reports."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, List

from sbp_observability.ai.ai_provider import AIProvider, NoopAIProvider
from sbp_observability.models import ErrorClass


def build_weekly_report(errors: Iterable[str], provider: AIProvider | None = None) -> str:
    provider = provider or NoopAIProvider()
    classified: List[ErrorClass] = provider.classify_errors(errors)
    counts = Counter(err.name for err in classified)
    lines = ["## Итоги недели по СБП", "", "### Топ проблем"]
    for name, count in counts.items():
        lines.append(f"- {name}: {count}")
    lines.append("")
    lines.append("### Рекомендации")
    lines.append("- Проверьте подключения банков-партнёров")
    return "\n".join(lines)
