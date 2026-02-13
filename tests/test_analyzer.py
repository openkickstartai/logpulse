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


def test_analyze_error_rate():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    assert stats["error_rate"] == 40.0  # 2 errors out of 5
    assert stats["error_count"] == 2


def test_analyze_hourly():
    entries = detect_and_parse(APACHE_LINES)
    stats = analyze(entries)
    assert "hourly_traffic" in stats
    assert len(stats["hourly_traffic"]) > 0


def test_analyze_single_pass_with_generator():
    """analyze() must work with a one-shot generator (proves single-pass)."""
    from logpulse.analyzer import analyze
    from logpulse.models import LogEntry

    entries = [
        LogEntry(ip="1.2.3.4", timestamp="15/Jan/2024:10:00:00 +0000",
                 method="GET", url="/index.html", status=200, size=1024),
        LogEntry(ip="5.6.7.8", timestamp="15/Jan/2024:10:05:00 +0000",
                 method="POST", url="/api/data", status=500, size=512),
        LogEntry(ip="1.2.3.4", timestamp="15/Jan/2024:11:00:00 +0000",
                 method="GET", url="/favicon.ico", status=404, size=0),
    ]

    def one_shot_gen():
        """A generator can only be consumed once — proves single-pass."""
        yield from entries

    stats = analyze(one_shot_gen(), top_n=5)
    assert stats["total_requests"] == 3
    assert stats["unique_ips"] == 2
    assert stats["error_count"] == 2        # 500 + 404
    assert stats["error_rate"] == 66.7      # round(2/3*100, 1)
    assert stats["total_bytes"] == 1536
    assert stats["top_ips"][0] == ("1.2.3.4", 2)
    assert len(stats["hourly_traffic"]) == 2  # 10:00 and 11:00
