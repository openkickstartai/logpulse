"""Shared test fixtures for logpulse tests."""
import pytest

APACHE_LINES = [
    "192.168.1.100 - - [15/Jan/2024:10:15:30 +0000] \"GET /index.html HTTP/1.1\" 200 1234 \"https://example.com\" \"Mozilla/5.0\"",
    "10.0.0.55 - - [15/Jan/2024:10:16:00 +0000] \"POST /api/users HTTP/1.1\" 201 89 \"-\" \"curl/7.88\"",
    "192.168.1.100 - - [15/Jan/2024:11:20:00 +0000] \"GET /style.css HTTP/1.1\" 304 0 \"https://example.com\" \"Mozilla/5.0\"",
    "172.16.0.1 - - [15/Jan/2024:11:25:00 +0000] \"GET /missing HTTP/1.1\" 404 162 \"-\" \"Mozilla/5.0\"",
    "10.0.0.55 - - [15/Jan/2024:12:00:00 +0000] \"DELETE /api/users/5 HTTP/1.1\" 500 44 \"-\" \"curl/7.88\""
]

JSON_LINES = [
    "{\"remote_addr\": \"192.168.1.1\", \"time\": \"2024-01-15T10:00:00Z\", \"method\": \"GET\", \"url\": \"/\", \"status\": 200, \"body_bytes_sent\": 512}",
    "{\"remote_addr\": \"10.0.0.1\", \"time\": \"2024-01-15T10:01:00Z\", \"method\": \"POST\", \"url\": \"/login\", \"status\": 401, \"body_bytes_sent\": 28}",
    "{\"remote_addr\": \"192.168.1.1\", \"time\": \"2024-01-15T10:02:00Z\", \"method\": \"GET\", \"url\": \"/dashboard\", \"status\": 200, \"body_bytes_sent\": 2048}"
]


@pytest.fixture
def apache_lines():
    return APACHE_LINES[:]


@pytest.fixture
def json_lines():
    return JSON_LINES[:]
