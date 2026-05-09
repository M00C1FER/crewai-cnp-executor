from decimal import Decimal

from crewai_cnp_executor.bidder_adapter import CrewAIBidderAdapter


class DummyAgent:
    def execute_task(self, task: str) -> str:
        return f"done:{task}"


def test_bidder_adapter_bids_and_executes() -> None:
    adapter = CrewAIBidderAdapter(agent=DummyAgent(), name="researcher", bid_price=Decimal("0.40"))

    assert adapter.bid("collect sources") == Decimal("0.40")
    assert adapter.execute("collect sources") == "done:collect sources"
