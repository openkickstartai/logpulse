"""Analyze parsed log entries and compute statistics."""
from collections import Counter
from logpulse.models import LogEntry
from typing import List, Dict, Any


def analyze(entries: List[LogEntry], top_n: int = 10) -> Dict[str, Any]:
    total = len(entries)
    ips = Counter(e.ip for e in entries)
    urls = Counter(e.url for e in entries)
    statuses = Counter(e.status for e in entries)
    methods = Counter(e.method for e in entries)
    total_bytes = sum(e.size for e in entries)

    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "total_bytes": total_bytes,
        "top_ips": ips.most_common(top_n),
        "top_urls": urls.most_common(top_n),
        "status_codes": sorted(statuses.items()),
        "methods": sorted(methods.items()),
    }
