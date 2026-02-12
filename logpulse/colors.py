"""ANSI color utilities for terminal output."""
import sys


_color_support_cache = None


def supports_color() -> bool:
    """Check if stdout supports ANSI colors (cached)."""
    global _color_support_cache
    if _color_support_cache is None:
        _color_support_cache = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    return _color_support_cache


GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def colorize(text: str, color: str) -> str:
    if not supports_color():
        return text
    return f"{color}{text}{RESET}"


def status_color(code: int) -> str:
    """Return appropriate color for HTTP status code."""
    if code < 300:
        return GREEN
    elif code < 400:
        return YELLOW
    else:
        return RED
