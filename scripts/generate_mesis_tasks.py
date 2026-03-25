#!/usr/bin/env python3
"""Generate 5x100 MESIS task specs from task family definitions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

LEVEL_ROTATION = {
    "A": [1, 2, 3, 4],
    "B": [2, 3, 5],
    "C": [2, 3, 5],
    "D": [1, 2, 3, 5],
    "E": [3, 4, 5],
}


def build_task(family: dict, index: int) -> dict:
    category = family["category"]
    level_cycle = LEVEL_ROTATION[category]
    level = level_cycle[(index - 1) % len(level_cycle)]
    slug = family["name"]
    task_id = f"{slug}_{index:03d}"

    return {
        "id": task_id,
        "name": f"{family['name']} task {index:03d}",
        "category": category,
        "level": level,
        "description": family["task_definition"],
        "io": {
            "stdin": [
                {"line_1": "control_instruction"},
                {"line_2": "target_program_or_config"},
                {"remaining": "runtime_payload"}
            ],
            "stdout": ["exact_result"]
        },
        "constraints": [
            "deterministic_output",
            "no_extra_whitespace",
            "no_debug_prints"
        ],
        "environment": family["environment_dependencies"],
        "validation": family["validation_scheme"],
        "generator_params": {
            "template_keys": family["generation"]["template_keys"],
            "variant_index": index
        },
        "tests": [
            {
                "name": "sanity",
                "input": "engine\nprogram\n1\n",
                "expected": "1"
            }
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MESIS tasks")
    parser.add_argument(
        "--families",
        type=Path,
        default=Path("mesis/task_families.json"),
        help="Path to task family definition JSON"
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("mesis/generated"),
        help="Output directory for generated task JSON files"
    )
    args = parser.parse_args()

    payload = json.loads(args.families.read_text())
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "benchmark": payload["benchmark"],
        "target_tasks_per_category": payload["target_tasks_per_category"],
        "generated": []
    }

    for family in payload["categories"]:
        category_name = family["name"]
        count = family["generation"]["count"]
        target_dir = args.out_dir / category_name
        target_dir.mkdir(parents=True, exist_ok=True)

        for idx in range(1, count + 1):
            task = build_task(family, idx)
            path = target_dir / f"{task['id']}.json"
            path.write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n")
            manifest["generated"].append(str(path))

    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Generated {len(manifest['generated'])} tasks into {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
