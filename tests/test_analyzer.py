"""Tests for log analyzer."""
from logpulse.analyzer import analyze
from logpulse.parsers import detect_and_parse
from tests.conftest import APACHE_LINES


def test_analyze_basic():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries, top_n=3)
    assert stats["total_requests"] == 5
    assert stats["unique_ips"] == 3
    assert len(stats["top_ips"]) == 3
    # 192.168.1.100 appears twice, 10.0.0.55 appears twice
    top_ip = stats["top_ips"][0][0]
    assert top_ip in ("192.168.1.100", "10.0.0.55")


def test_analyze_status_codes():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    codes = dict(stats["status_codes"])
    assert 200 in codes
    assert 201 in codes
    assert 304 in codes
    assert 404 in codes
    assert 500 in codes
    assert sum(codes.values()) == 5


def test_analyze_top_n():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries, top_n=1)
    assert len(stats["top_ips"]) == 1
    assert len(stats["top_urls"]) == 1
