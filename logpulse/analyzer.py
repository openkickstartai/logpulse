"""Analyze parsed log entries and compute statistics."""
import re
from collections import Counter
from logpulse.models import LogEntry
from typing import Iterable, Dict, Any



def _extract_hour(timestamp: str) -> str:
    """Extract hour string from various timestamp formats."""
    m = re.search(r"(\d{2}):\d{2}:\d{2}", timestamp)
    if m:
        return f"{m.group(1)}:00"
    return "unknown"

def analyze(entries: Iterable[LogEntry], top_n: int = 10) -> Dict[str, Any]:
    """Single-pass analysis over log entries.

    Accepts any Iterable (including generators), so callers can
    stream entries without buffering the full list in memory.
    Previous impl did 7+ full passes; this does exactly 1.
    """
    ips: Counter = Counter()
    urls: Counter = Counter()
    statuses: Counter = Counter()
    methods: Counter = Counter()
    hours: Counter = Counter()
    error_urls: Counter = Counter()
    total = 0
    total_bytes = 0
    error_count = 0

    for e in entries:
        total += 1
        ips[e.ip] += 1
        urls[e.url] += 1
        statuses[e.status] += 1
        methods[e.method] += 1
        total_bytes += e.size
        hours[_extract_hour(e.timestamp)] += 1
        if e.status >= 400:
            error_count += 1
            error_urls[e.url] += 1

    hourly_traffic = sorted(hours.items())
    error_rate = round(error_count / total * 100, 1) if total else 0

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "total_bytes": total_bytes,
        "top_ips": ips.most_common(top_n),
        "top_urls": urls.most_common(top_n),
        "status_codes": sorted(statuses.items()),
        "methods": sorted(methods.items()),
        "hourly_traffic": hourly_traffic,
        "error_rate": error_rate,
        "error_count": error_count,
        "error_urls": error_urls.most_common(top_n),
    }

    }
