"""Format analysis results for output."""
import json as json_mod
from typing import Dict, Any


def _fmt_num(n: int) -> str:
    return f"{n:,}"


def report(stats: Dict[str, Any], fmt: str = "table", errors_only: bool = False) -> str:
    if fmt == "json":
        if errors_only:
            error_stats = {
                "error_rate": stats.get("error_rate", 0),
                "error_count": stats.get("error_count", 0),
                "error_urls": stats.get("error_urls", []),
                "total_requests": stats["total_requests"],
            }
            return json_mod.dumps(error_stats, indent=2, default=str)
        return json_mod.dumps(stats, indent=2, default=str)
    if errors_only:
        return _error_report(stats)
    return _table_report(stats)


def _error_report(stats: Dict[str, Any]) -> str:
    lines = []
    lines.append("")
    lines.append(" logpulse error report")
    lines.append("\u2500" * 48)
    total = stats["total_requests"]
    err_count = stats.get("error_count", 0)
    err_rate = stats.get("error_rate", 0)
    lines.append(f"  Total requests:  {_fmt_num(total)}")
    lines.append(f"  Error count:     {_fmt_num(err_count)}")
    lines.append(f"  Error rate:      {err_rate:.1f}%")
    lines.append("")
    lines.append("  Top Error URLs:")
    for url, count in stats.get("error_urls", []):
        display_url = (url[:40] + "...") if len(url) > 40 else url
        lines.append(f"    {display_url:<44s} {_fmt_num(count):>8s} errors")
    return "\n".join(lines)


def _table_report(stats: Dict[str, Any]) -> str:
    lines = []
    lines.append("")
    lines.append(" logpulse report")
    lines.append("\u2500" * 48)
    total = stats["total_requests"]
    lines.append(f"  Total requests:  {_fmt_num(total)}")
    lines.append(f"  Unique IPs:      {_fmt_num(stats['unique_ips'])}")
    lines.append(f"  Total bytes:     {_fmt_num(stats['total_bytes'])}")
    if stats.get("error_rate") is not None:
        lines.append(f"  Error rate:      {stats['error_rate']:.1f}%")
    lines.append("")

    lines.append("  Status Codes:")
    for code, count in stats["status_codes"]:
        pct = (count / total * 100) if total else 0
        lines.append(f"    {code}  {_fmt_num(count):>8s}  ({pct:5.1f}%)")
    lines.append("")

    if stats.get("hourly_traffic"):
        lines.append("  Hourly Traffic:")
        for hour, count in stats["hourly_traffic"]:
            bar = "\u2588" * min(count, 40)
            lines.append(f"    {hour}  {bar} {_fmt_num(count)}")
        lines.append("")

    geo_data = stats.get("top_ips_geo")
    if geo_data:
        lines.append("  Top IPs:")
        for ip, count, country in geo_data:
            lines.append(f"    {ip:<20s} {_fmt_num(count):>8s} reqs  ({country})")
    else:
        lines.append("  Top IPs:")
        for ip, count in stats["top_ips"]:
            lines.append(f"    {ip:<20s} {_fmt_num(count):>8s} reqs")
    lines.append("")

    lines.append("  Top URLs:")
    for url, count in stats["top_urls"]:
        display_url = (url[:40] + "...") if len(url) > 40 else url
        lines.append(f"    {display_url:<44s} {_fmt_num(count):>8s}")

    if stats.get("error_urls"):
        lines.append("")
        lines.append("  Top Error URLs:")
        for url, count in stats["error_urls"]:
            display_url = (url[:40] + "...") if len(url) > 40 else url
            lines.append(f"    {display_url:<44s} {_fmt_num(count):>8s} errors")

    return "\n".join(lines)
