# crewai-cnp-executor

`crewai-cnp-executor` is a lightweight shim that lets CrewAI workflows dispatch tasks through Contract Net Protocol (CNP) semantics from `contract-net-router`, bringing formal lifecycle states and budget conservation into CrewAI-native orchestration without forking CrewAI.

## Install + quick start

Install with pip, then wrap CrewAI-style agents as bidders and dispatch under a parent budget.

```bash
pip install crewai-cnp-executor
```

```python
from decimal import Decimal

from crewai_cnp_executor import CNPProcess, CrewAIBidderAdapter

class Agent:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute_task(self, task: str) -> str:
        return f"{self.name}: {task}"

process = CNPProcess(
    bidders=[
        CrewAIBidderAdapter(Agent("analyst"), "analyst", Decimal("0.40")),
        CrewAIBidderAdapter(Agent("writer"), "writer", Decimal("0.30")),
        CrewAIBidderAdapter(Agent("reviewer"), "reviewer", Decimal("0.30")),
    ],
    total_budget=Decimal("1.00"),
)

awards = process.dispatch([
    ("subtask-a", Decimal("0.40")),
    ("subtask-b", Decimal("0.30")),
    ("subtask-c", Decimal("0.30")),
])
```

## Decision matrix

| Use case | Vanilla CrewAI | `crewai-cnp-executor` |
|---|---|---|
| Simple linear or hierarchical plans without strict budget constraints | ✅ Best fit | ⚪ Optional |
| Need explicit contract lifecycle state tracking (`FULFILLED`, `VIOLATED`, etc.) | ⚪ Limited | ✅ Recommended |
| Must enforce parent-budget conservation during decomposition | ⚪ Manual | ✅ Built-in |
| Want formal CNP dispatch semantics while keeping CrewAI workflow style | ⚪ Not native | ✅ Designed for this |

## Upstream and research context

- Dispatch backend: [`M00C1FER/contract-net-router`](https://github.com/M00C1FER/contract-net-router)
- Motivation: *Agent Contracts* (arXiv: [2601.08815](https://arxiv.org/abs/2601.08815), COINE 2026)

### Dependency note

This scaffold is designed to consume lifecycle-state support from `contract-net-router` (including work tracked in `M00C1FER/contract-net-router#4`). If your environment uses a pre-merge router build, pin to a compatible upstream revision until the lifecycle API is released.

> Follow-up: add a reciprocal cross-link from the `contract-net-router` README back to this shim.
