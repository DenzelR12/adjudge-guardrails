import argparse
import json
from pathlib import Path

from adjudge.metrics import MetricRecord, effective_status


def load(path: str) -> list[MetricRecord]:
    return [MetricRecord.model_validate(item) for item in json.loads(Path(path).read_text())]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["freshness", "verify"])
    parser.add_argument("--registry", required=True)
    args = parser.parse_args()
    records, failed = load(args.registry), False
    for record in records:
        status = effective_status(record)
        print(f"{record.metric_id}: {status}")
        failed = failed or (args.command == "verify" and status != "verified")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
