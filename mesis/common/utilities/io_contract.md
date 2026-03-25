# MESIS I/O Contract

## Input

Each execution task consumes standard input in the following form:

- **Line 1:** control instruction (e.g., interpreter identifier or entrypoint path)
- **Line 2:** target program/configuration
- **Line 3+:** runtime input payload forwarded according to task routing rules

## Output

Implementations must produce:

- exact expected output,
- no additional debug text,
- deterministic formatting,
- stable newline behavior.

## Routing Semantics

When tasks involve multiple layers (interpreter-in-interpreter, VM-in-VM, or DSL pipeline), forwarding behavior must be explicit in the task spec:

- which layer consumes each input segment,
- whether input is partitioned or broadcast,
- whether output from an inner layer is transformed or forwarded verbatim.

## Enforcement

Public tests should verify baseline correctness while hidden tests should stress:

- nested depth handling,
- edge-case input partitioning,
- semantic equivalence between direct and interpreted execution.
