"""Data models for parsed log entries."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    ip: str
    timestamp: str
    method: str
    url: str
    status: int
    size: int
    referer: Optional[str] = None
    user_agent: Optional[str] = None
