from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class BudgetTracker:
    """Tracks budget consumption for contract awards."""

    total: Decimal
    spent: Decimal = field(default=Decimal("0.00"))

    def can_allocate(self, amount: Decimal) -> bool:
        """Return True when amount can be allocated without violating budget."""
        return self.spent + amount <= self.total

    def allocate(self, amount: Decimal) -> bool:
        """Reserve amount from budget and return whether allocation succeeded."""
        if not self.can_allocate(amount):
            return False
        self.spent += amount
        return True

    @property
    def remaining(self) -> Decimal:
        """Current remaining budget."""
        return self.total - self.spent
