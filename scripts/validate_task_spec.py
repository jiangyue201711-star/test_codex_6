#!/usr/bin/env python3
"""Minimal validator for MESIS JSON task specs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = {
    "id",
    "name",
    "category",
    "level",
    "description",
    "io",
    "constraints",
    "tests",
}

VALID_CATEGORIES = {"A", "B", "C", "D", "E"}
VALID_LEVELS = {1, 2, 3, 4, 5}


def validate_task(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text())
    except Exception as exc:  # pragma: no cover - defensive
        return [f"{path}: failed to parse JSON: {exc}"]

    if not isinstance(payload, dict):
        return [f"{path}: root must be a mapping"]

    missing = sorted(REQUIRED_TOP_LEVEL - set(payload.keys()))
    if missing:
        errors.append(f"{path}: missing required fields: {', '.join(missing)}")

    category = payload.get("category")
    if category not in VALID_CATEGORIES:
        errors.append(f"{path}: invalid category '{category}' (expected one of {sorted(VALID_CATEGORIES)})")

    level = payload.get("level")
    if level not in VALID_LEVELS:
        errors.append(f"{path}: invalid level '{level}' (expected 1-5)")

    io_field = payload.get("io")
    if not isinstance(io_field, dict) or "stdin" not in io_field or "stdout" not in io_field:
        errors.append(f"{path}: io must include 'stdin' and 'stdout'")

    tests = payload.get("tests")
    if not isinstance(tests, list) or not tests:
        errors.append(f"{path}: tests must be a non-empty list")
    else:
        for idx, test in enumerate(tests):
            if not isinstance(test, dict):
                errors.append(f"{path}: tests[{idx}] must be a mapping")
                continue
            for req in ("name", "expected"):
                if req not in test:
                    errors.append(f"{path}: tests[{idx}] missing '{req}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MESIS task spec files.")
    parser.add_argument("files", nargs="+", type=Path, help="JSON task files to validate")
    args = parser.parse_args()

    all_errors: list[str] = []
    for file_path in args.files:
        all_errors.extend(validate_task(file_path))

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
