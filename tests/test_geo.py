"""Tests for IP geolocation module."""
from unittest.mock import patch, MagicMock
from logpulse.geo import lookup_ip, enrich_top_ips, _cache


def setup_function():
    _cache.clear()


def test_private_ip():
    assert lookup_ip("192.168.1.1") == "Private/Local"
    assert lookup_ip("10.0.0.1") == "Private/Local"
    assert lookup_ip("127.0.0.1") == "Private/Local"


def test_cache_hit():
    _cache["8.8.8.8"] = "United States"
    assert lookup_ip("8.8.8.8") == "United States"


@patch("logpulse.geo.urllib.request.urlopen")
def test_lookup_public_ip(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = b'{"country_name": "Germany"}'
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_urlopen.return_value = mock_resp
    result = lookup_ip("1.2.3.4")
    assert result == "Germany"
    assert _cache["1.2.3.4"] == "Germany"


@patch("logpulse.geo.urllib.request.urlopen")
def test_lookup_failure(mock_urlopen):
    mock_urlopen.side_effect = Exception("network error")
    result = lookup_ip("1.2.3.4")
    assert result is None


def test_enrich_top_ips():
    top_ips = [("192.168.1.1", 100), ("10.0.0.5", 50)]
    enriched = enrich_top_ips(top_ips)
    assert len(enriched) == 2
    assert enriched[0] == ("192.168.1.1", 100, "Private/Local")
    assert enriched[1] == ("10.0.0.5", 50, "Private/Local")
