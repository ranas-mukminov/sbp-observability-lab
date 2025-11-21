from sbp_observability.ai import error_classifier


def test_classifier_matches_base_rules():
    errors = ["gateway timeout", "bank decline"]
    classified = error_classifier.classify(errors)
    assert classified[0].name == "GATEWAY_TIMEOUT"
    assert classified[1].name == "BANK_DECLINE"
