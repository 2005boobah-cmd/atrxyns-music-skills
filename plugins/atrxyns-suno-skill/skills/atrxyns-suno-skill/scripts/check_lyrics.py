"""Check an exact UTF-8 lyrics field against an exclusive character limit."""
import argparse
import json
from pathlib import Path


def measure(text, limit=5000):
    if not isinstance(text, str):
        raise ValueError('lyrics must be a string')
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError('limit must be a positive integer')
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    code_points = len(normalized)
    utf16_units = len(normalized.encode("utf-16-le")) // 2
    crlf_upper_bound = utf16_units + normalized.count("\n")
    largest = max(code_points, utf16_units, crlf_upper_bound)
    return {
        "code_points": code_points,
        "utf16_units": utf16_units,
        "crlf_upper_bound": crlf_upper_bound,
        "exclusive_limit": limit,
        "pass": largest < limit,
        "remaining_safe_characters": max(0, limit - 1 - largest),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="UTF-8 file containing only lyrics")
    parser.add_argument("--limit", type=int, default=5000)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be positive")
    try:
        text = args.path.read_bytes().decode("utf-8-sig")
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"Cannot read lyrics: {exc}\n")
    result = measure(text, args.limit)
    print(json.dumps(result, ensure_ascii=True))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
