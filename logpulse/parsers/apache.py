"""Apache Combined Log Format parser."""
import re
from logpulse.models import LogEntry
from typing import Optional

APACHE_PATTERN = re.compile(
    r"(?P<ip>[\d.]+) - - "
    r"\[(?P<timestamp>[^\]]+)\] "
    r"\"(?P<method>\w+) (?P<url>[^ ]+) HTTP/[^\"]+\" "
    r"(?P<status>\d+) (?P<size>\d+|-)"
    r"(?: \"(?P<referer>[^\"]*)\" \"(?P<ua>[^\"]*)\")?"   
)


def parse_apache(line: str) -> Optional[LogEntry]:
    m = APACHE_PATTERN.match(line)
    if not m:
        return None
    size = int(m.group("size")) if m.group("size") != "-" else 0
    return LogEntry(
        ip=m.group("ip"),
        timestamp=m.group("timestamp"),
        method=m.group("method"),
        url=m.group("url"),
        status=int(m.group("status")),
        size=size,
        referer=m.group("referer"),
        user_agent=m.group("ua"),
    )
