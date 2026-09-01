import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from adjudge.metrics import MetricRecord, effective_status
from adjudge.report import WaiverRecord, build_report


def load(path: str) -> list[MetricRecord]:
    return [MetricRecord.model_validate(item) for item in json.loads(Path(path).read_text())]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["freshness", "verify", "report"])
    parser.add_argument("--registry", required=True)
    parser.add_argument("--waivers")
    parser.add_argument("--as-of", dest="as_of")
    args = parser.parse_args()
    records, failed = load(args.registry), False
    if args.command == "report":
        registry_text = Path(args.registry).read_text()
        waivers_text = Path(args.waivers).read_text() if args.waivers else "[]"
        try:
            waivers = [WaiverRecord.model_validate(item) for item in json.loads(waivers_text)]
        except (ValidationError, json.JSONDecodeError) as error:
            print(f"report failed closed: waiver registry is malformed: {error}", file=sys.stderr)
            return 2
        as_of = datetime.fromisoformat(args.as_of) if args.as_of else None
        print(build_report(records, waivers, registry_text, waivers_text, as_of))
        return 0
    for record in records:
        status = effective_status(record)
        print(f"{record.metric_id}: {status}")
        failed = failed or (args.command == "verify" and status != "verified")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
