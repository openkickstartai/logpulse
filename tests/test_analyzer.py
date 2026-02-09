"""Tests for log analyzer."""
from logpulse.analyzer import analyze
from logpulse.parsers import detect_and_parse
from tests.conftest import APACHE_LINES


def test_analyze_basic():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries, top_n=3)
    assert stats["total_requests"] == 5
    assert stats["unique_ips"] == 3  # 192.168.1.100, 10.0.0.55, 172.16.0.1
    assert len(stats["top_ips"]) == 3
    assert stats["top_ips"][0] == ("192.168.1.100", 2)  # most frequent


def test_analyze_status_codes():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    codes = dict(stats["status_codes"])
    assert codes[200] == 1
    assert codes[404] == 1
    assert codes[500] == 1


def test_analyze_top_n():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries, top_n=1)
    assert len(stats["top_ips"]) == 1
    assert len(stats["top_urls"]) == 1
