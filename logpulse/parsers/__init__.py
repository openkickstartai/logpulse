"""Log parsers module."""
from logpulse.parsers.apache import parse_apache
from logpulse.parsers.nginx import parse_nginx
from logpulse.parsers.json_log import parse_json_log
from logpulse.models import LogEntry
from typing import List


def detect_and_parse(lines: list) -> List[LogEntry]:
    """Try each parser and return entries from the first one that works."""
    sample = lines[:5]

    # Try JSON first (most specific)
    json_results = []
    for line in sample:
        entry = parse_json_log(line)
        if entry:
            json_results.append(entry)
    if len(json_results) >= len(sample) * 0.5:
        entries = []
        for line in lines:
            e = parse_json_log(line)
            if e:
                entries.append(e)
        return entries

    # Try Apache Combined
    apache_results = [parse_apache(l) for l in sample]
    if sum(1 for r in apache_results if r) >= len(sample) * 0.5:
        return [e for e in (parse_apache(l) for l in lines) if e]

    # Try nginx
    nginx_results = [parse_nginx(l) for l in sample]
    if sum(1 for r in nginx_results if r) >= len(sample) * 0.5:
        return [e for e in (parse_nginx(l) for l in lines) if e]

    return []
