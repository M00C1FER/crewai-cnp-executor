from decimal import Decimal

from crewai_cnp_executor import CNPProcess, CrewAIBidderAdapter


class DemoAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    def execute_task(self, task: str) -> str:
        return f"{self.name} -> {task}"


if __name__ == "__main__":
    bidders = [
        CrewAIBidderAdapter(DemoAgent("researcher"), "researcher", Decimal("0.40")),
        CrewAIBidderAdapter(DemoAgent("writer"), "writer", Decimal("0.30")),
        CrewAIBidderAdapter(DemoAgent("editor"), "editor", Decimal("0.30")),
    ]
    process = CNPProcess(bidders=bidders, total_budget=Decimal("1.00"))
    awards = process.dispatch(
        [
            ("gather sources", Decimal("0.40")),
            ("draft summary", Decimal("0.30")),
            ("review output", Decimal("0.30")),
        ]
    )
    for award in awards:
        print(award)
