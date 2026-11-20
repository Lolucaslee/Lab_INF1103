from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """
    Represents a virtual item delivered electronically via internet download.
    Does NOT implement CanBeShipped interface.
    """

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        """Getter for download file size in MB."""
        return self._download_size

    @download_size.setter
    def download_size(self, value: float) -> None:
        """Setter for download file size with validation."""
        if value < 0:
            raise ValueError("Download size cannot be negative.")
        self._download_size = float(value)

    def display_information(self) -> None:
        """
        Method Overriding: Reuses parent base information and appends 
        download size.
        """
        super().display_information()
        print(f" | Download Size: {self._download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        """Concrete implementation of the abstract method from Product."""
        return f"Item delivered via direct digital download link (Size: {self._download_size} MB)."

    def to_dict(self) -> dict:
        """Extends parent dictionary serialization with type and size info."""
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self._download_size
        return data