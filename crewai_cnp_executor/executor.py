from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Sequence

from .bidder_adapter import CrewAIBidderAdapter
from .budget import BudgetTracker

try:
    from contract_net_router import ContractState as RouterContractState
except Exception:
    RouterContractState = None


if RouterContractState is not None:
    ContractState = RouterContractState
else:

    class ContractState(str, Enum):
        PENDING = "PENDING"
        AWARDED = "AWARDED"
        FULFILLED = "FULFILLED"
        VIOLATED = "VIOLATED"


@dataclass
class ContractAward:
    task: str
    bidder: str
    amount: Decimal
    state: ContractState
    result: str | None = None


class CNPProcess:
    """CrewAI process adapter that awards tasks under CNP-style budget controls."""

    def __init__(
        self,
        bidders: Sequence[CrewAIBidderAdapter],
        total_budget: Decimal,
        router: Any | None = None,
    ) -> None:
        self.bidders = list(bidders)
        self.budget = BudgetTracker(total=total_budget)
        self.router = router

    def award_contract(self, task: str, max_amount: Decimal, bidder_index: int = 0) -> ContractAward:
        """Award a task to a bidder if budget allows, otherwise mark violated."""
        bidder = self.bidders[bidder_index]
        bid_amount = bidder.bid(task)
        amount = min(max_amount, bid_amount)

        if not self.budget.allocate(amount):
            return ContractAward(
                task=task,
                bidder=bidder.name,
                amount=amount,
                state=ContractState.VIOLATED,
                result=None,
            )

        if self.router is not None and hasattr(self.router, "award_contract"):
            self.router.award_contract(task=task, bidder=bidder.name, amount=float(amount))

        result = bidder.execute(task)
        return ContractAward(
            task=task,
            bidder=bidder.name,
            amount=amount,
            state=ContractState.FULFILLED,
            result=result,
        )

    def dispatch(self, tasks: Sequence[tuple[str, Decimal]]) -> list[ContractAward]:
        """Dispatch tasks in order to bidders by index position."""
        awards: list[ContractAward] = []
        for idx, (task, amount) in enumerate(tasks):
            bidder_index = min(idx, len(self.bidders) - 1)
            awards.append(self.award_contract(task=task, max_amount=amount, bidder_index=bidder_index))
        return awards
