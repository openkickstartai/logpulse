"""CLI entry point for logpulse."""
import sys
import click
from logpulse.parsers import detect_and_parse
from logpulse.analyzer import analyze
from logpulse.reporter import report


@click.command()
@click.argument("logfile", type=click.Path(exists=True), default="-")
@click.option("--format", "fmt", type=click.Choice(["table", "json"]), default="table", help="Output format")
@click.option("--top", "top_n", default=10, help="Number of top entries to show")
@click.option("--errors-only", is_flag=True, help="Show only error analysis (4xx/5xx)")
@click.option("--geo", is_flag=True, help="Resolve top IPs to country (uses ipapi.co)")
def main(logfile, fmt, top_n, errors_only, geo):
    """Analyze log files and generate summary reports."""
    if logfile == "-":
        lines = sys.stdin.read().splitlines()
    else:
        with open(logfile) as f:
            lines = f.read().splitlines()

    if not lines:
        click.echo("No log lines found.", err=True)
        raise SystemExit(1)

    entries = detect_and_parse(lines)
    if not entries:
        click.echo("Could not parse any log entries. Check the format.", err=True)
        raise SystemExit(1)

    stats = analyze(entries, top_n=top_n)

    # Enrich with geo data if requested
    if geo:
        from logpulse.geo import enrich_top_ips
        stats["top_ips_geo"] = enrich_top_ips(stats["top_ips"])

    output = report(stats, fmt=fmt, errors_only=errors_only)
    click.echo(output)


if __name__ == "__main__":
    main()
