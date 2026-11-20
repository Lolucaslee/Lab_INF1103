from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """
    Strategy pattern: the common interface every discount shares.
    Order only ever calls apply(); it never needs to know which discount it has.
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Takes an order total and returns the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) is 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(total - self.amount, 0.0)
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy (Section 2.4): 5% off. Added WITHOUT changing Order."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
