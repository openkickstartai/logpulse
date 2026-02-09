# logpulse

A lightweight CLI log analyzer for quick server debugging.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Analyze a log file
logpulse access.log

# Pipe from stdin
cat /var/log/nginx/access.log | logpulse -

# JSON output
logpulse access.log --format json

# Show top 20 IPs
logpulse access.log --top 20
```

## Supported Formats

- Apache Combined Log Format
- nginx default access log
- JSON structured logs (one object per line)

## Output Example

```
 logpulse report — access.log
────────────────────────────────────
 Total requests: 12,847
 Unique IPs:     342
 Time range:     2024-01-15 00:00 → 2024-01-15 23:59

 Status Codes:
   200  10,234  (79.7%)
   304   1,456  (11.3%)
   404     892  ( 6.9%)
   500     265  ( 2.1%)

 Top 10 IPs:
   192.168.1.100    1,847 reqs
   10.0.0.55        1,203 reqs
   ...
```

## Contributing

Contributions welcome! Check the task board for open tasks.

## License

MIT
