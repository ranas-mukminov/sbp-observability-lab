from typer.testing import CliRunner

from sbp_observability.cli.main import app


def test_parse_logs_command(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text("2024-01-01T00:00:00 [alpha] [mobile] payment 200 0.120\n")
    runner = CliRunner()
    result = runner.invoke(app, ["parse-logs", str(log_file), "--format", "nginx"])
    assert result.exit_code == 0


def test_generate_weekly_report_command(tmp_path):
    data_file = tmp_path / "errors.txt"
    data_file.write_text("timeout\ndecline\n")
    runner = CliRunner()
    result = runner.invoke(app, ["generate-weekly-report", str(data_file)])
    assert "Итоги недели" in result.stdout
