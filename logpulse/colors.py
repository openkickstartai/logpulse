"""ANSI color utilities for terminal output."""
import sys
from functools import lru_cache


@lru_cache(maxsize=1)
def supports_color() -> bool:
    """Check if stdout supports ANSI colors (cached)."""
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


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


@lru_cache(maxsize=128)
def status_color(code: int) -> str:
    """Return appropriate color for HTTP status code (cached)."""
    if code < 300:
        return GREEN
    elif code < 400:
        return YELLOW
    else:
        return RED
