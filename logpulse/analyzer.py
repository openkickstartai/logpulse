"""Analyze parsed log entries and compute statistics."""
import re
from collections import Counter
from logpulse.models import LogEntry
from typing import List, Dict, Any


def _extract_hour(timestamp: str) -> str:
    """Extract hour string from various timestamp formats."""
    if not timestamp or not isinstance(timestamp, str):
        return "unknown"
    
    try:
        m = re.search(r"(\d{2}):\d{2}:\d{2}", timestamp)
        if m:
            return f"{m.group(1)}:00"
    except (AttributeError, TypeError):
        pass
    return "unknown"


def analyze(entries: List[LogEntry], top_n: int = 10) -> Dict[str, Any]:
    if not entries or not isinstance(entries, list):
        return {
            "total_requests": 0,
            "unique_ips": 0,
            "total_bytes": 0,
            "top_ips": [],
            "top_urls": [],
            "status_codes": [],
            "methods": [],
            "hourly_traffic": [],
            "error_rate": 0.0,
            "error_urls": []
        }
    
    # Filter out invalid entries
    valid_entries = [e for e in entries if hasattr(e, 'ip') and hasattr(e, 'url') and hasattr(e, 'status')]
    total = len(valid_entries)
    
    if total == 0:
        return {
            "total_requests": 0,
            "unique_ips": 0,
            "total_bytes": 0,
            "top_ips": [],
            "top_urls": [],
            "status_codes": [],
            "methods": [],
            "hourly_traffic": [],
            "error_rate": 0.0,
            "error_urls": []
        }
    
    try:
        ips = Counter(e.ip for e in valid_entries if e.ip)
        urls = Counter(e.url for e in valid_entries if e.url)
        statuses = Counter(e.status for e in valid_entries if hasattr(e, 'status') and e.status is not None)
        methods = Counter(e.method for e in valid_entries if hasattr(e, 'method') and e.method)
        
        # Safe byte calculation
        total_bytes = 0
        for e in valid_entries:
            if hasattr(e, 'size') and e.size is not None:
                try:
                    total_bytes += int(e.size)
                except (ValueError, TypeError):
                    continue
        
        hours = Counter(_extract_hour(e.timestamp) for e in valid_entries if hasattr(e, 'timestamp'))
        hourly_traffic = sorted(hours.items())

        # Error analysis with validation
        errors = []
        for e in valid_entries:
            try:
                if hasattr(e, 'status') and e.status is not None and int(e.status) >= 400:
                    errors.append(e)
            except (ValueError, TypeError):
                continue
        
        error_rate = round(len(errors) / total * 100, 1) if total > 0 else 0.0
        error_urls = Counter(e.url for e in errors if hasattr(e, 'url') and e.url).most_common(top_n)

        return {
            "total_requests": total,
            "unique_ips": len(ips),
            "total_bytes": total_bytes,
            "top_ips": ips.most_common(top_n),
            "top_urls": urls.most_common(top_n),
            "status_codes": statuses.most_common(top_n),
            "methods": methods.most_common(top_n),
            "hourly_traffic": hourly_traffic,
            "error_rate": error_rate,
            "error_urls": error_urls
        }
    except Exception as e:
        # Fallback response on unexpected errors
        return {
            "total_requests": len(valid_entries),
            "unique_ips": 0,
            "total_bytes": 0,
            "top_ips": [],
            "top_urls": [],
            "status_codes": [],
            "methods": [],
            "hourly_traffic": [],
            "error_rate": 0.0,
            "error_urls": [],
            "error": f"Analysis failed: {str(e)}"
        }
