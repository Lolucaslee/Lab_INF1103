from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """
    Interface contract defining shipping capabilities ('must-be-able-to').
    Does not hold attributes or implementation details, only method requirements.
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns the shipping cost for the item."""
        pass