from dataclasses import dataclass


@dataclass(frozen=True)
class ContractResult:
    valid: bool
    errors: tuple[str, ...] = ()


def validate_required_columns(rows: list[dict], required: set[str]) -> ContractResult:
    if not rows:
        return ContractResult(False, ("source returned no rows",))
    available = set(rows[0])
    missing = tuple(sorted(required - available))
    return ContractResult(not missing, tuple(f"missing required column: {name}" for name in missing))


def validate_non_null(rows: list[dict], fields: set[str]) -> ContractResult:
    errors = tuple(f"null value: row={index}, field={field}" for index, row in enumerate(rows) for field in fields if row.get(field) is None)
    return ContractResult(not errors, errors)
