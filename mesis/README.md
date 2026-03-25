# MESIS: Meta-Execution & Self-Interpretation Suite

MESIS is a benchmark suite for evaluating advanced program reasoning in LLMs through metacircular interpretation, multi-stage execution, self-hosting, and strict I/O semantics.

## Scope

MESIS covers five categories:

- **Category A:** Meta-interpreter tasks
- **Category B:** Virtual machine tasks
- **Category C:** Multi-layer execution pipelines
- **Category D:** I/O routing and control flow
- **Category E:** Self-referential and adversarial programs

Difficulty levels range from Level 1 (basic interpretation) to Level 5 (adversarial multi-layer execution).

## Repository Layout

```text
mesis/
├── category_a/
│   ├── level_1/
│   ├── level_3/
│   └── level_4/
├── category_b/
├── category_c/
├── category_d/
├── category_e/
├── common/
│   ├── runtimes/
│   ├── interpreters/
│   └── utilities/
└── tests/
    ├── public/
    └── hidden/
```

## I/O Contract

All tasks consume structured `STDIN` with deterministic output requirements.

1. Line 1: Control instruction (interpreter/runtime selector)
2. Line 2: Program path or task configuration
3. Remaining lines: Runtime payload forwarded to the selected execution stack

Outputs must:

- match exact expected result,
- avoid extra whitespace,
- avoid debug logs,
- remain deterministic.

See `common/utilities/io_contract.md` for details.

## Task Metadata

Each task should provide a machine-readable spec. A starter schema is available in `task_spec_schema.json`, and a sample task is included at `tests/public/eval_scm_self_host.json`.

## Validation

Use the helper validator for local checks:

```bash
python3 scripts/validate_task_spec.py mesis/tests/public/eval_scm_self_host.json
```

The validator checks required keys and structural consistency for core fields (`id`, `category`, `level`, `io`, and `tests`).

## Planned Evaluation Metrics

- pass rate per category,
- pass rate per difficulty level,
- max successful interpretation depth,
- failure-mode distribution (`parsing_error`, `environment_error`, `recursion_failure`, `io_misrouting`).

## 5类任务定义与批量生成（每类100个）

`task_families.json` 已定义 A-E 五类任务的：

- 任务定义（task definition）
- 所依赖环境（environment dependencies）
- 验证方案（validation scheme）
- 生成配置（generation.count = 100）

执行下面命令即可一次性生成 500 个任务：

```bash
python3 scripts/generate_mesis_tasks.py
```

输出目录：`mesis/generated/`，并包含 `manifest.json`。
