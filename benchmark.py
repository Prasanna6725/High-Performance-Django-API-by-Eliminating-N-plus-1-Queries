import argparse
import json
import statistics
import time
from pathlib import Path

import requests


def benchmark(url, request_count):
    durations = []
    query_counts = []

    for _ in range(request_count):
        started = time.perf_counter()
        response = requests.get(url, timeout=60)
        elapsed_ms = (time.perf_counter() - started) * 1000
        response.raise_for_status()
        durations.append(elapsed_ms)
        query_counts.append(int(response.headers.get("X-DB-Query-Count", "-1")))

    return {
        "query_count": query_counts[0],
        "avg_response_ms": round(statistics.fmean(durations), 3),
        "min_response_ms": round(min(durations), 3),
        "max_response_ms": round(max(durations), 3),
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark a Django API endpoint.")
    parser.add_argument("url", help="Endpoint to benchmark")
    parser.add_argument("--requests", type=int, default=50, dest="request_count")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()

    result = benchmark(args.url, args.request_count)
    print(json.dumps(result, indent=2))

    if args.output:
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
