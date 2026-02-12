"""Analyze parsed log entries and compute statistics."
import re
from collections import Counter
from logpulse.models import LogEntry
from typing import List, Dict, Any


def _extract_hour(timestamp: str) -> str:
    """Extract hour string from various timestamp formats."
    m = re.search(r"(\d{2}):\d{2}:\d{2}", timestamp)
    if m:
        return f"{m.group(1)}:00"
    return "unknown"


def analyze(entries: List[LogEntry], top_n: int = 10) -> Dict[str, Any]:
    total = len(entries)
    ips = Counter(e.ip for e in entries)
    urls = Counter(e.url for e in entries)
    statuses = Counter(e.status for e in entries)
    methods = Counter(e.method for e in entries)
    total_bytes = sum(e.size for e in entries)
    hours = Counter(_extract_hour(e.timestamp) for e in entries)
    hourly_traffic = sorted(hours.items())

    # Error analysis
    errors = [e for e in entries if e.status >= 400]
    error_rate = round(len(errors) / total * 100, 1) if total else 0
    error_urls = Counter(e.url for e in errors).most_common(top_n)

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
        "error_count": len(errors),
        "error_urls": error_urls,
    }