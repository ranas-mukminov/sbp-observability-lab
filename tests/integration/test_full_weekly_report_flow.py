from sbp_observability.ai.report_generator import build_weekly_report
from sbp_observability.ai.ai_provider import NoopAIProvider


def test_weekly_report_flow():
    errors = ["timeout", "decline", "timeout"]
    report = build_weekly_report(errors, provider=NoopAIProvider())
    assert "GATEWAY_TIMEOUT" in report
    assert "BANK_DECLINE" in report
