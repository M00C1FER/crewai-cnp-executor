from decimal import Decimal

from crewai_cnp_executor.bidder_adapter import CrewAIBidderAdapter
from crewai_cnp_executor.executor import CNPProcess, ContractState


class FakeCrewAIAgent:
    def __init__(self, role: str) -> None:
        self.role = role

    def execute_task(self, task: str) -> str:
        return f"{self.role} completed {task}"


def _build_process() -> CNPProcess:
    bidders = [
        CrewAIBidderAdapter(FakeCrewAIAgent("analyst"), "analyst", Decimal("0.40")),
        CrewAIBidderAdapter(FakeCrewAIAgent("writer"), "writer", Decimal("0.30")),
        CrewAIBidderAdapter(FakeCrewAIAgent("reviewer"), "reviewer", Decimal("0.30")),
    ]
    return CNPProcess(bidders=bidders, total_budget=Decimal("1.00"))


def test_integration_three_subtasks_fulfilled_within_budget() -> None:
    process = _build_process()
    awards = process.dispatch(
        [
            ("task-1", Decimal("0.40")),
            ("task-2", Decimal("0.30")),
            ("task-3", Decimal("0.30")),
        ]
    )

    assert [award.state for award in awards] == [
        ContractState.FULFILLED,
        ContractState.FULFILLED,
        ContractState.FULFILLED,
    ]
    assert process.budget.remaining == Decimal("0.00")


def test_integration_fourth_subtask_violated_at_award_time() -> None:
    process = _build_process()
    awards = process.dispatch(
        [
            ("task-1", Decimal("0.40")),
            ("task-2", Decimal("0.30")),
            ("task-3", Decimal("0.30")),
            ("task-4", Decimal("0.30")),
        ]
    )

    assert [award.state for award in awards[:3]] == [
        ContractState.FULFILLED,
        ContractState.FULFILLED,
        ContractState.FULFILLED,
    ]
    assert awards[3].state == ContractState.VIOLATED
    assert process.budget.remaining == Decimal("0.00")
