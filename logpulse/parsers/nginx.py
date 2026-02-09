"""nginx default access log parser.\n\nnginx default format is identical to Apache Combined in most setups,\nso we reuse the Apache parser but also handle the nginx-specific\n$request_time field if present.\n"""
import re
from logpulse.models import LogEntry
from logpulse.parsers.apache import parse_apache
from typing import Optional


def parse_nginx(line: str) -> Optional[LogEntry]:
    # nginx default is basically Apache Combined
    return parse_apache(line)
