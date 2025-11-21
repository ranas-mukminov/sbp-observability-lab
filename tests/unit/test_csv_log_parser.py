from pathlib import Path

from sbp_observability.config import ParserConfig
from sbp_observability.parsing import csv_log_parser


def test_parse_csv_file(tmp_path: Path):
    content = "timestamp,bank_id,channel,operation_type,status,error_code,latency_ms\n"
    content += "2024-01-01T00:00:00,alpha,mobile,payment,success,,120\n"
    file_path = tmp_path / "sample.csv"
    file_path.write_text(content)
    events = csv_log_parser.parse_file(file_path)
    assert len(events) == 1
    assert events[0].latency_ms == 120


def test_parse_with_mapping(tmp_path: Path):
    content = "ts,bank_alias,channel,operation_type,status,error_code,latency_ms\n"
    content += "2024-01-01T00:00:00,alpha,mobile,payment,success,,120\n"
    file_path = tmp_path / "sample.csv"
    file_path.write_text(content)
    config = ParserConfig(column_mapping={"timestamp": "ts", "bank_id": "bank_alias"})
    events = csv_log_parser.parse_file(file_path, config)
    assert events[0].bank_id == "alpha"
