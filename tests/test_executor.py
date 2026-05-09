from decimal import Decimal

from crewai_cnp_executor.bidder_adapter import CrewAIBidderAdapter
from crewai_cnp_executor.executor import CNPProcess, ContractState


class DummyAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute_task(self, task: str) -> str:
        return f"{self.name}:{task}"


def test_award_contract_violates_when_budget_exceeded() -> None:
    process = CNPProcess(
        bidders=[CrewAIBidderAdapter(DummyAgent("a"), "a", Decimal("0.30"))],
        total_budget=Decimal("0.20"),
    )

    award = process.award_contract(task="over-budget", max_amount=Decimal("0.30"))

    assert award.state == ContractState.VIOLATED
    assert process.budget.remaining == Decimal("0.20")
