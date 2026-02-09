"""IP geolocation lookup using ipapi.co free API."""
import json
import urllib.request
import urllib.error
from typing import Dict, Optional

_cache: Dict[str, Optional[str]] = {}


def lookup_ip(ip: str) -> Optional[str]:
    """Look up the country for an IP address.
    Uses ipapi.co free tier (no API key, 1000 requests/day).
    Returns country name or None on failure.
    """
    if ip.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.",
                      "172.20.", "172.21.", "172.22.", "172.23.", "172.24.",
                      "172.25.", "172.26.", "172.27.", "172.28.", "172.29.",
                      "172.30.", "172.31.", "192.168.", "127.", "0.")):
        return "Private/Local"
    if ip in _cache:
        return _cache[ip]
    try:
        url = f"https://ipapi.co/{ip}/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "logpulse/0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            country = data.get("country_name")
            _cache[ip] = country
            return country
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, OSError):
        _cache[ip] = None
        return None


def enrich_top_ips(top_ips: list) -> list:
    """Add country info to top IPs list.
    Returns list of (ip, count, country) tuples.
    """
    enriched = []
    for ip, count in top_ips:
        country = lookup_ip(ip)
        enriched.append((ip, count, country or "Unknown"))
    return enriched
