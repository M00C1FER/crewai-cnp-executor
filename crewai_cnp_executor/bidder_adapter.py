from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class CrewAIBidderAdapter:
    """Wraps a CrewAI-compatible agent as a bidder."""

    agent: Any
    name: str
    bid_price: Decimal

    def bid(self, task: str) -> Decimal:
        """Return bid amount for the task."""
        _ = task
        return self.bid_price

    def execute(self, task: str) -> str:
        """Execute the task through the wrapped agent."""
        if hasattr(self.agent, "execute_task"):
            return str(self.agent.execute_task(task))
        if hasattr(self.agent, "run"):
            return str(self.agent.run(task))
        if callable(self.agent):
            return str(self.agent(task))
        raise TypeError("Wrapped agent does not support execute_task, run, or __call__")
