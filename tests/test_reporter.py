"""Tests for report formatter."""
import json
from logpulse.reporter import report
from logpulse.analyzer import analyze
from logpulse.parsers import detect_and_parse
from tests.conftest import APACHE_LINES


def test_table_report():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    output = report(stats, fmt="table")
    assert "logpulse report" in output
    assert "Total requests" in output
    assert "5" in output
    assert "Status Codes" in output


def test_json_report():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    output = report(stats, fmt="json")
    data = json.loads(output)
    assert data["total_requests"] == 5
    assert "top_ips" in data
    assert "status_codes" in data


def test_error_report():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    output = report(stats, fmt="table", errors_only=True)
    assert "error report" in output
    assert "Error rate" in output
