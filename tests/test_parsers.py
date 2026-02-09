"""Tests for log parsers."""
from logpulse.parsers.apache import parse_apache
from logpulse.parsers.json_log import parse_json_log
from logpulse.parsers import detect_and_parse
from tests.conftest import APACHE_LINES, JSON_LINES


def test_parse_apache_valid():
    entry = parse_apache(APACHE_LINES[0])
    assert entry is not None
    assert entry.ip == "192.168.1.100"
    assert entry.method == "GET"
    assert entry.url == "/index.html"
    assert entry.status == 200
    assert entry.size == 1234


def test_parse_apache_post():
    entry = parse_apache(APACHE_LINES[1])
    assert entry.method == "POST"
    assert entry.status == 201


def test_parse_apache_malformed():
    assert parse_apache("this is not a log line") is None
    assert parse_apache("") is None


def test_parse_json_valid():
    entry = parse_json_log(JSON_LINES[0])
    assert entry is not None
    assert entry.ip == "192.168.1.1"
    assert entry.status == 200
    assert entry.url == "/"


def test_parse_json_invalid():
    assert parse_json_log("not json") is None
    assert parse_json_log("{}") is None


def test_detect_apache():
    entries = detect_and_parse(APACHE_LINES)
    assert len(entries) == 5
    assert entries[0].ip == "192.168.1.100"


def test_detect_json():
    entries = detect_and_parse(JSON_LINES)
    assert len(entries) == 3
    assert entries[0].ip == "192.168.1.1"


def test_detect_empty():
    assert detect_and_parse([]) == []
