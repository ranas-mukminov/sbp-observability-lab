from sbp_observability.ai import report_generator
from sbp_observability.ai.ai_provider import NoopAIProvider


def test_build_weekly_report_contains_sections():
    errors = ["timeout", "decline", "other"]
    report = report_generator.build_weekly_report(errors, provider=NoopAIProvider())
    assert "Итоги недели" in report
    assert "Топ проблем" in report
