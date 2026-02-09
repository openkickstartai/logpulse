"""JSON structured log parser."""
import json
from logpulse.models import LogEntry
from typing import Optional


def parse_json_log(line: str) -> Optional[LogEntry]:
    try:
        obj = json.loads(line.strip())
    except (json.JSONDecodeError, ValueError):
        return None

    # Common JSON log field names
    ip = obj.get("remote_addr") or obj.get("ip") or obj.get("client_ip") or ""
    ts = obj.get("timestamp") or obj.get("time") or obj.get("@timestamp") or ""
    method = obj.get("method") or obj.get("request_method") or "GET"
    url = obj.get("url") or obj.get("path") or obj.get("request_uri") or "/"
    status = int(obj.get("status") or obj.get("status_code") or obj.get("response_code") or 0)
    size = int(obj.get("body_bytes_sent") or obj.get("bytes") or obj.get("size") or 0)

    if not ip or not status:
        return None

    return LogEntry(
        ip=ip,
        timestamp=str(ts),
        method=method,
        url=url,
        status=status,
        size=size,
    )
